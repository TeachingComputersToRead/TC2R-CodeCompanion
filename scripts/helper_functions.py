import fitz
import pandas as pd
import pytesseract
from pytesseract import Output
from PIL import Image
import spacy
import os
import matplotlib.pyplot as plt
from typing import List
from bs4 import BeautifulSoup
import pickle

def pdf_to_text_with_ocr(pdf_path: str, output_txt_path: str):
    """
    Behavior:  The filename of the PDF is used to create two automatically saved output
    files - a text file and an Excel file - to the designated folder.
    Any errors are printed to the screen.

    Parameters:
    - pdf_path (str): filepath to the PDF on local disk
    - output_txt_path (str): filepath to the folder in which to save

    Returns: None

    ## Example usage:
    # pdf_file_path = os.path.join(HOME_DIRECTORY, "test.pdf")
    # output_text_file_path = os.path.join(HOME_DIRECTORY, text_files)
    # pdf_to_text_with_ocr(pdf_file_path, output_text_file_path)
    """
    try:
        # Open the PDF file using PyMuPDF
        pdf_document = fitz.open(pdf_path)
        pdf_name = os.path.basename(pdf_path) + '.txt'
        excel_name = os.path.basename(pdf_path) + '.xlsx'

        # Initialize an empty string to store the text content
        text_content = ""
        # Initialize an empty pandas db to store positions
        positions_df = pd.DataFrame()

        # Iterate through each page in the PDF
        for page_num in range(pdf_document.page_count):
            # Get the current page
            page = pdf_document[page_num]

            # Render the page as an image
            image = page.get_pixmap()
            img = Image.frombytes("RGB", (image.width, image.height), image.samples)

            # Perform OCR using pytesseract on the image
            page_text = pytesseract.image_to_string(img, lang='eng')
            positions = pytesseract.image_to_data(img, output_type=Output.DATAFRAME)

            # Append the extracted text to the overall content
            text_content += page_text
            positions_df = pd.concat([positions_df, positions], ignore_index=True)

        # Save the text content to a text file
        with open(os.path.join(output_txt_path, pdf_name), 'w', encoding='utf-8') as txt_file:
            txt_file.write(text_content)

        # Save positions to spreadsheet
        positions_df.to_excel(os.path.join(output_txt_path, excel_name), index=False)

        # Print a success message
        print(f"OCR completed successfully. Text saved at: {os.path.join(output_txt_path, pdf_name)}")

    except OSError as err:
        print("OS error:", err)
    except ValueError as err:
        print("URL or folder is invalid:", err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def pull_text_from_html(file_list):
    """
    Extracts and cleans text content from a list of HTML files.

    This function iterates through a list of file paths, attempts to open each file,
    and handles potential encoding errors by first trying 'windows-1252' and then
    'utf-8'. It then uses BeautifulSoup to parse the HTML content and extract
    all text, joining it into a single, clean string.

    Args:
        file_list (list): A list of file paths to HTML documents.

    Returns:
        list: A list of strings, where each string contains the cleaned text
              content from the corresponding HTML file.
    """
    clean_texts = []

    # Iterate through each file path provided in the list
    for f in file_list:
        html_string = ''  # Initialize an empty string to hold the HTML content

        # First, try to open the file using the 'windows-1252' encoding
        try:
            with open(f, 'r', encoding='windows-1252') as file:
                html_string = file.read()
        except Exception as e1:
            print(f'Encoding error with windows-1252 for file {f}: {e1}')

            # If 'windows-1252' fails, try 'utf-8' encoding
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    html_string = file.read()
                    print(f'Successfully read file {f} with utf-8 encoding.')
            except Exception as e2:
                print(f'Encoding error with utf-8 for file {f}: {e2}')
                # If both encodings fail, the html_string remains empty, and the loop continues.

        # Use BeautifulSoup to parse the HTML and extract all text
        # .stripped_strings removes leading/trailing whitespace and empty strings
        # ' '.join() combines all the extracted strings into one single string
        if html_string:  # Only proceed if we successfully read content
            clean_text = ' '.join(BeautifulSoup(html_string, "html.parser").stripped_strings)
            clean_texts.append(clean_text)
        else:
            clean_texts.append(None)  # Append None or an empty string if file couldn't be read

    return clean_texts


def read_text_files(folder_path: str):
    """
    Behavior: Read text from a folder of .txt files, ignoring other file types

    Parameters:
    - folder_path (str): Path to the folder containing .txt files.

    Returns:
    - texts (list): List of strings, where each string is the content of a text file.
    """
    texts = []
    files = []

    # Add a check to see if the folder exists
    if not os.path.isdir(folder_path):
        return texts, files

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                texts.append(text)
                files.append(filename)
        else:
            print('Skipping', filename, ', which is not a text file and will be excluded from analysis.')
    return texts, files


def calculate_ocr_quality(texts: List):
    """
    Behavior: Calculate OCR quality scores for a list of texts based on recognized English words.

    Parameters:
    - texts (list): List of OCR-generated texts.

    Returns:
    - ocr_quality_scores (list): List of OCR quality scores ranging from 0 to 1
    """
    nlp = spacy.load("en_core_web_sm")
    ocr_quality_scores = []

    for text in texts:
        doc = nlp(text)
        english_word_count = sum(1 for token in doc if token.is_alpha and token.text.lower() in nlp.vocab)
        total_word_count = len(doc)

        # Calculate OCR quality as the ratio of recognized English words to total words
        quality_score = english_word_count / total_word_count if total_word_count > 0 else 0
        ocr_quality_scores.append(quality_score)

    return ocr_quality_scores


def plot_ocr_quality_histogram(ocr_quality_scores: List, output_folder: str):
    """
    Behavior: Plot a histogram of OCR quality scores.

    Parameters:
    - ocr_quality_scores (list): List of OCR quality scores ranging from 0 to 1

    Returns: None
    """
    # Check if OCR quality scores are provided
    if not ocr_quality_scores:
        print("Error: No OCR quality scores provided.")
        return

    # Plot the histogram
    plt.hist(ocr_quality_scores, bins=20, range=(0, 1), edgecolor='black', alpha=0.7)

    # Set labels and title
    plt.title('OCR Quality Histogram')
    plt.xlabel('OCR Quality Score')
    plt.ylabel('Frequency')

    # Show the plot
    plt.savefig(os.path.join(output_folder, "OCR_quality_distribution.png"))
    return

def process_texts_to_dataframe(texts: List, filenames: List):
    """
    Tokenize sentences in a list of texts and save the results in a Pandas DataFrame.

    Parameters:
    - texts (list): List of texts to be processed.
    - filenames (list): List of corresponding filenames.

    Returns:
    - df (DataFrame): Pandas DataFrame containing columns: 'filename', 'sentence_index', 'sentence_text'.
    """
    nlp = spacy.load('en_core_web_sm', exclude=["parser"])
    config = {"punct_chars": ['\n\n', '.', '?', '!']}
    nlp.add_pipe("sentencizer", config=config)

    data = {'filename': [], 'sentence_index': [], 'sentence_text': []}

    for filename, text in zip(filenames, texts):
        for i, sentence in enumerate(nlp(text).sents):
            data['filename'].append(filename)
            data['sentence_index'].append(i)
            data['sentence_text'].append(sentence.text)

    df = pd.DataFrame(data)
    return df


def run_classification_model(df: pd.DataFrame, model_folder: str,
                             model_name: str = "ml_classifier_gbc.pkl",
                             threshold: float=0.5) -> pd.DataFrame:
    """
    Loads a pre-trained machine learning model and uses it to predict
    the top sentence from each document.

    This function takes a DataFrame with text embeddings, loads a specified
    model from a given folder, and applies the model to predict a probability
    score for each sentence. It then identifies the sentence with the highest
    probability score within each document (filename) and returns a new DataFrame
    with these top predictions.

    Args:
        df (pd.DataFrame): The input DataFrame. It must contain 'filename',
                           and 'Embedding' columns. The 'Embedding' column should
                           contain numerical representations (e.g., word embeddings or
                           TF-IDF vectors) of the text.
        model_folder (str): The path to the directory where the pre-trained model file is stored.
        model_name (str, optional): The name of the pickled model file.
                                     Defaults to "ml_classifier_gbc.pkl".
        threshold (float, optional): Probability threshold below which to ignore/mask model predictions

    Returns:
        pd.DataFrame: A DataFrame containing the top predicted sentences for each
                      unique filename, along with their corresponding probability scores.
    """
    # Load the pre-trained classification model using pickle
    model_path = os.path.join(model_folder, model_name)
    with open(model_path, 'rb') as f:
        clf_model = pickle.load(f)

    # Use the loaded model to predict the probability for each sentence's embedding.
    # The [:, 1] is used to get the probabilities of the positive class.
    df['Probability'] = clf_model.predict_proba(df['Embedding'].to_list())[:, 1]

    # Find the index of the row with the maximum 'Probability' for each 'filename'.
    # This identifies the top-scoring sentence for each document.
    top_doc_preds_indices = df.groupby('filename')['Probability'].idxmax()

    # Use the indices to select the corresponding rows from the original DataFrame.
    top_doc_preds = df.loc[top_doc_preds_indices].reset_index(drop=True)

    # Mask any rows with a probability less than a given prob threshold (default 0.5)
    mask = top_doc_preds['Probability'] < threshold
    cols_to_mask = ['sentence_index', 'sentence_text', 'Embedding', 'Probability']
    top_doc_preds.loc[mask, cols_to_mask] = pd.NA

    return top_doc_preds
