import glob
import os
import pickle
from sentence_transformers import SentenceTransformer
import argparse
import logging # Import the logging module

from helper_functions import pdf_to_text_with_ocr, pull_text_from_html, read_text_files, calculate_ocr_quality, plot_ocr_quality_histogram, process_texts_to_dataframe, run_classification_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the SentenceTransformer model for model input features. This model needs to be loaded once.
try:
    sent_emb_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    logging.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading SentenceTransformer model: {e}")
    exit(1)  # Exit if the model cannot be loaded

def process_and_classify_files(input_folder, output_folder, model_folder,
                               sent_emb_model = sent_emb_model, threshold=0.5):
    """
    Orchestrates the entire process of ingesting files, plotting OCR quality,
    running a classification model, and outputting the results.

    This function first identifies PDF and HTML files in the input folder and
    converts them to text files in a temporary 'text_files' directory. It then
    reads all text files, calculates and plots the OCR quality, processes the
    text into a DataFrame, classifies the sentences, identifies the top probability
    in each document and saves the final results to an Excel file.

    Args:
        input_folder (str): Path to the folder containing PDF and HTML files.
        output_folder (str): Path to the folder where the final Excel output
                             will be saved.
        model_folder (str): The path to the directory where the pre-trained model file is stored.
        sent_emb_model (SentenceTransformer): SentenceTransformer object that is used to create
                            embeddings which are used as input features for the model
        threshold (float, optional): Probability threshold below which to ignore/mask model predictions
    """
    logging.info(f"Starting file processing for input folder: {input_folder}")

    # Create a directory for text file output
    text_dir = os.path.join(output_folder, 'text_files')
    os.makedirs(text_dir, exist_ok=True)
    logging.info(f"Ensured text files directory exists at: {text_dir}")

    # 1. Ingest PDF and HTML files
    logging.info("Ingesting files...")
    # Process PDFs with OCR
    pdf_files = glob.glob(os.path.join(input_folder, '*.pdf'))
    for pdf_file in pdf_files:
        try:
            pdf_to_text_with_ocr(pdf_file, text_dir)
            logging.info(f"Successfully processed PDF file: {pdf_file}")
        except Exception as e:
            logging.error(f"Error processing PDF file {pdf_file}: {e}")

    # Process HTML files
    html_files1 = glob.glob(os.path.join(input_folder, '*.html'))
    html_files2 = glob.glob(os.path.join(input_folder, '*.htm'))
    html_files = html_files1 + html_files2
    html_texts = pull_text_from_html(html_files)
    for html_file, text_content in zip(html_files, html_texts):
        if text_content:
            if html_file.lower().endswith('.html'):
                file_name = os.path.basename(html_file).replace('.html', '.txt')
            elif html_file.lower().endswith('.htm'):
                file_name = os.path.basename(html_file).replace('.htm', '.txt')
            output_file_path = os.path.join(text_dir, file_name)
            try:
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                logging.info(f"Successfully processed HTML file: {html_file} and saved to {output_file_path}")
            except Exception as e:
                logging.error(f"Error saving HTML content from {html_file} to {output_file_path}: {e}")
        else:
            logging.warning(f"No content extracted from HTML file: {html_file}. Skipping save.")

    # 2. Read all ingested text files
    logging.info("Reading ingested text files...")
    texts, filenames = read_text_files(text_dir)
    logging.info(f"Read {len(texts)} text files.")
    df = process_texts_to_dataframe(texts, filenames)
    logging.info("Processed texts into DataFrame.")
    df['Embedding'] = df['sentence_text'].apply(lambda x: sent_emb_model.encode(x))
    logging.info("Generated sentence embeddings.")

    # Save DataFrame for debugging/future use
    data_df_path = os.path.join(output_folder, 'data_df.pkl')
    try:
        with open(data_df_path, 'wb') as pkl:
            pickle.dump(df, pkl)
        logging.info(f"DataFrame with embeddings saved to: {data_df_path}")
    except Exception as e:
        logging.error(f"Error saving DataFrame to {data_df_path}: {e}")


    # 3. Create output plot of OCR quality
    logging.info("Calculating and plotting OCR quality...")
    ocr_scores = calculate_ocr_quality(texts)
    plot_ocr_quality_histogram(ocr_scores, output_folder)
    logging.info("OCR quality histogram generated.")

    # 4. Run classification model
    logging.info("Processing texts and running classification model...")
    df_model_results = run_classification_model(df, model_folder, threshold=threshold)
    logging.info("Classification model run successfully.")

    # 5. Output the results to Excel
    output_excel_path = os.path.join(output_folder, 'model_results.xlsx')
    try:
        df_model_results.to_excel(output_excel_path, index=False)
        logging.info(f"Classification results saved to: {output_excel_path}")
    except Exception as e:
        logging.error(f"Error saving classification results to {output_excel_path}: {e}")

    logging.info("File processing and classification pipeline finished.")
    return df_model_results


# --- Main execution block ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process PDF/HTML files, calculate OCR quality, and run a classification model."
    )
    # Add arguments for the function parameters
    parser.add_argument(
        "--input_folder",
        type=str,
        required=True,
        help="Path to the folder containing PDF and HTML files."
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        required=True,
        help="Path to the folder where the final Excel output and temporary text files will be saved."
    )
    parser.add_argument(
        "--model_folder",
        type=str,
        required=True,
        help="Path to the directory where the pre-trained classification model file is stored."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Probability threshold below which to ignore/mask model predictions (default: 0.5)."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main processing function with the parsed arguments
    logging.info("\n--- Starting File Processing and Classification Pipeline ---")
    results_df = process_and_classify_files(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        model_folder=args.model_folder,
        sent_emb_model=sent_emb_model,
        threshold=args.threshold
    )
    logging.info("\n--- Pipeline Execution Finished ---")
    if results_df is not None:
        logging.info(f"Results DataFrame head:\n{results_df.head()}")
    else:
        logging.warning("No results DataFrame was returned.")

### Example use
# python pipeline.py --input_folder=./tests/docs --output_folder=./tests/ --model_folder=./tests/model
