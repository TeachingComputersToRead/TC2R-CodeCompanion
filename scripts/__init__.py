# scripts/__init__.py

# Makes main functions available directly from the python package
from .pipeline import process_and_classify_files
from .helper_functions import pdf_to_text_with_ocr, pull_text_from_html, \
    read_text_files, calculate_ocr_quality, plot_ocr_quality_histogram, \
    process_texts_to_dataframe, run_classification_model

# Define the package version
__version__ = "0.1.0"