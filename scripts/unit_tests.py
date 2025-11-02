import unittest
import os
import shutil
from helper_functions import pdf_to_text_with_ocr, pull_text_from_html, read_text_files

class TestPdfToTextWithOcr(unittest.TestCase):
    """
    Unit tests for the pdf_to_text_with_ocr function.
    """

    def setUp(self):
        """
        Set up the directory structure for the test. This test assumes
        a 'docs' folder already exists and contains the necessary input files.
        It creates a new 'test_output' sub-directory within 'docs' for test results.
        """
        # Define the base directory for input files (the existing 'docs' folder)
        self.input_dir = 'tests/docs'

        # Define the directory where output files will be saved
        self.output_dir = os.path.join(self.input_dir, 'test_output')

        # Create the output directory.
        os.makedirs(self.output_dir, exist_ok=True)

        # Define the path for the pre-existing PDF file.
        # This file MUST exist in the 'docs' folder for the test to run successfully.
        self.test_pdf_path = os.path.join(self.input_dir, '{0A9CB96C-5A24-4881-97F4-4D0BCFB29CC5}.pdf')
        self.test_empty_pdf_path = os.path.join(self.input_dir, 'empty.pdf')
        self.test_irrelevant_file_path = os.path.join(self.input_dir, 'not_a_pdf.pdf')

        # Create dummy empty and irrelevant files for testing edge cases
        with open(self.test_empty_pdf_path, 'w') as f:
            pass  # Create an empty file

        with open(self.test_irrelevant_file_path, 'w') as f:
            f.write("This is not a PDF file.")

        # Verify that the required input file exists.
        if not os.path.exists(self.test_pdf_path):
            self.fail(f"Required test PDF not found. Please place '{os.path.basename(self.test_pdf_path)}' "
                      f"in the '{self.input_dir}' folder to run this test.")

    def tearDown(self):
        """
        Cleans up the temporary files and folders created by the test,
        except for the original input files in the 'docs' folder.
        """
        # Remove the temporary output directory
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        # Remove the dummy files created for testing
        if os.path.exists(self.test_empty_pdf_path):
            os.remove(self.test_empty_pdf_path)
        if os.path.exists(self.test_irrelevant_file_path):
            os.remove(self.test_irrelevant_file_path)

    def test_successful_execution(self):
        """
        Tests the successful execution of pdf_to_text_with_ocr with a valid input.
        Verifies that the function creates both a text file and an Excel file in
        the designated output folder.
        """
        # 1. Arrange: Define the expected output file paths based on the input PDF name.
        file_name_base = os.path.basename(self.test_pdf_path)
        expected_txt_path = os.path.join(self.output_dir, file_name_base + '.txt')
        expected_xlsx_path = os.path.join(self.output_dir, file_name_base + '.xlsx')

        # 2. Act: Call the function with the path to the existing PDF and the output directory.
        pdf_to_text_with_ocr(self.test_pdf_path, self.output_dir)

        # 3. Assert: Verify the expected behavior.

        # Check that the output text file was created.
        self.assertTrue(os.path.exists(expected_txt_path),
                        f"Expected text file not found at {expected_txt_path}")

        # Check that the output Excel file was created.
        self.assertTrue(os.path.exists(expected_xlsx_path),
                        f"Expected Excel file not found at {expected_xlsx_path}")

        # Check that the created files are not empty.
        self.assertGreater(os.path.getsize(expected_txt_path), 0,
                           "Output text file is empty, suggesting an issue with OCR or content extraction.")
        self.assertGreater(os.path.getsize(expected_xlsx_path), 0,
                           "Output Excel file is empty.")

    def test_error_handling_nonexistent_file(self):
        """
        Tests error handling of pdf_to_text_with_ocr when given a nonexistent PDF file.
        Verifies that the function raises an exception and no output files are created.
        """
        # 1. Arrange: Define the path to a file that does not exist.
        nonexistent_pdf_path = os.path.join(self.input_dir, 'nonexistent_file.pdf')

        # Define the paths for the output files that should NOT be created.
        file_name_base = os.path.basename(nonexistent_pdf_path)
        expected_txt_path = os.path.join(self.output_dir, file_name_base + '.txt')
        expected_xlsx_path = os.path.join(self.output_dir, file_name_base + '.xlsx')

        # 2. Act & Assert (part 1): Verify that calling the function with the bad path raises an exception.
        with self.assertRaises(Exception):
            pdf_to_text_with_ocr(nonexistent_pdf_path, self.output_dir)

        # 3. Assert (part 2): Verify that no output files were created.
        self.assertFalse(os.path.exists(expected_txt_path),
                         f"Unexpectedly found output text file at {expected_txt_path}")
        self.assertFalse(os.path.exists(expected_xlsx_path),
                         f"Unexpectedly found output Excel file at {expected_xlsx_path}")

    def test_error_handling_empty_or_irrelevant_file(self):
        """
        Tests error handling for both empty files and irrelevant file types.
        Verifies that the function raises an exception and no output files are created.
        """
        # Test Case 1: Empty PDF file
        # Define the paths for the output files that should NOT be created.
        file_name_base_empty = os.path.basename(self.test_empty_pdf_path)
        expected_txt_path_empty = os.path.join(self.output_dir, file_name_base_empty + '.txt')
        expected_xlsx_path_empty = os.path.join(self.output_dir, file_name_base_empty + '.xlsx')

        # Verify that calling the function with the empty file raises an exception.
        with self.assertRaises(Exception):
            pdf_to_text_with_ocr(self.test_empty_pdf_path, self.output_dir)

        # Verify that no output files were created.
        self.assertFalse(os.path.exists(expected_txt_path_empty),
                         f"Unexpectedly found output text file for empty input at {expected_txt_path_empty}")
        self.assertFalse(os.path.exists(expected_xlsx_path_empty),
                         f"Unexpectedly found output Excel file for empty input at {expected_xlsx_path_empty}")

        # Test Case 2: Irrelevant file type with a .pdf extension
        # Define the paths for the output files that should NOT be created.
        file_name_base_irrelevant = os.path.basename(self.test_irrelevant_file_path)
        expected_txt_path_irrelevant = os.path.join(self.output_dir, file_name_base_irrelevant + '.txt')
        expected_xlsx_path_irrelevant = os.path.join(self.output_dir, file_name_base_irrelevant + '.xlsx')

        # Verify that calling the function with the irrelevant file raises an exception.
        with self.assertRaises(Exception):
            pdf_to_text_with_ocr(self.test_irrelevant_file_path, self.output_dir)

        # Verify that no output files were created.
        self.assertFalse(os.path.exists(expected_txt_path_irrelevant),
                         f"Unexpectedly found output text file for irrelevant input at {expected_txt_path_irrelevant}")
        self.assertFalse(os.path.exists(expected_xlsx_path_irrelevant),
                         f"Unexpectedly found output Excel file for irrelevant input at {expected_xlsx_path_irrelevant}")


class TestPullTextFromHtml(unittest.TestCase):
    """
    Unit tests for the pull_text_from_html function.
    """

    def setUp(self):
        """
        Sets up the directory structure and creates dummy files for testing.
        """
        # Define a temporary test directory
        self.test_dir = 'test_html_env'
        os.makedirs(self.test_dir, exist_ok=True)

        # Create a valid HTML file with some content
        self.test_html_path_1 = os.path.join(self.test_dir, 'test1.html')
        with open(self.test_html_path_1, 'w') as f:
            f.write("<html><body><p>This is test content.</p></body></html>")

        # Create another valid HTML file with different content
        self.test_html_path_2 = os.path.join(self.test_dir, 'test2.html')
        with open(self.test_html_path_2, 'w') as f:
            f.write("<html><body><h1>Another test</h1><p>And more content.</p></body></html>")

        # Create an empty HTML file
        self.test_empty_html_path = os.path.join(self.test_dir, 'empty.html')
        with open(self.test_empty_html_path, 'w') as f:
            pass

        # Create a nonexistent file path
        self.nonexistent_html_path = os.path.join(self.test_dir, 'nonexistent.html')

    def tearDown(self):
        """
        Cleans up the temporary test directory after the tests are complete.
        """
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_successful_execution(self):
        """
        Tests the successful extraction of text from a list of valid HTML files.
        """
        # 1. Arrange: Create a list of valid HTML file paths
        file_list = [self.test_html_path_1, self.test_html_path_2]

        # 2. Act: Call the function with the list of files
        extracted_texts = pull_text_from_html(file_list)

        # 3. Assert: Verify the returned list contains the expected cleaned text
        self.assertEqual(len(extracted_texts), 2)
        self.assertIn("This is test content.", extracted_texts)
        self.assertIn("Another test And more content.", extracted_texts)
        self.assertNotIn(None, extracted_texts)

    def test_error_handling_nonexistent_file(self):
        """
        Tests that the function returns None for a nonexistent file path.
        """
        # 1. Arrange: Create a list with a nonexistent file path
        file_list = [self.nonexistent_html_path]

        # 2. Act: Call the function with the list
        extracted_texts = pull_text_from_html(file_list)

        # 3. Assert: Verify the function returns a list with a single None
        self.assertEqual(len(extracted_texts), 1)
        self.assertEqual(extracted_texts[0], None)

    def test_error_handling_empty_or_mixed_files(self):
        """
        Tests that the function correctly handles a mix of valid, empty,
        and nonexistent files.
        """
        # 1. Arrange: Create a list with a mix of file paths
        file_list = [self.test_html_path_1, self.test_empty_html_path, self.nonexistent_html_path]

        # 2. Act: Call the function
        extracted_texts = pull_text_from_html(file_list)

        # 3. Assert: Verify the output is as expected
        self.assertEqual(len(extracted_texts), 3)
        self.assertEqual(extracted_texts[0], "This is test content.")
        self.assertEqual(extracted_texts[1], None)  # Empty file should return an empty string
        self.assertEqual(extracted_texts[2], None)


class TestReadTextFiles(unittest.TestCase):
    """
    Unit tests for the read_text_files function.
    """

    def setUp(self):
        """
        Sets up a temporary test directory with various test files.
        """
        self.test_dir = 'test_read_files_env'
        self.input_dir = os.path.join(self.test_dir, 'input_folder')
        os.makedirs(self.input_dir, exist_ok=True)

        # Create dummy text files for successful execution test
        with open(os.path.join(self.input_dir, 'file1.txt'), 'w') as f:
            f.write('This is the content of file one.')
        with open(os.path.join(self.input_dir, 'file2.txt'), 'w') as f:
            f.write('And this is the content of file two.')

        # Create non-text files for irrelevant file type tests
        with open(os.path.join(self.input_dir, 'image.jpg'), 'w') as f:
            f.write('This is an image file.')
        with open(os.path.join(self.input_dir, 'log.log'), 'w') as f:
            f.write('This is a log file.')

    def tearDown(self):
        """
        Cleans up the temporary test directory after tests are complete.
        """
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_successful_execution(self):
        """
        Tests that the function correctly reads multiple text files and returns a list
        of strings with the expected content.
        """
        # Read files and get the list of strings
        file_list, _ = read_text_files(self.input_dir)

        # Assert that the return value is a list
        self.assertIsInstance(file_list, list, "The function should return a list.")

        # Assert that the number of strings is correct
        self.assertEqual(len(file_list), 2, "List of files should contain 2 strings.")

        # Assert that the content of the strings is correct
        self.assertIn('This is the content of file one.', file_list)
        self.assertIn('And this is the content of file two.', file_list)

    def test_error_handling_nonexistent_folder(self):
        """
        Tests that the function handles a nonexistent folder gracefully and returns an empty list.
        """
        nonexistent_folder = os.path.join(self.test_dir, 'nonexistent_folder')
        file_list, _ = read_text_files(nonexistent_folder)
        self.assertIsInstance(file_list, list, "The function should return a list.")
        self.assertTrue(not file_list, "List of files should be empty for a nonexistent folder.")

    def test_edge_case_empty_folder(self):
        """
        Tests that the function handles an empty folder gracefully and returns an empty list.
        """
        empty_folder = os.path.join(self.test_dir, 'empty_folder')
        os.makedirs(empty_folder)
        file_list, _ = read_text_files(empty_folder)
        self.assertIsInstance(file_list, list, "The function should return a list.")
        self.assertTrue(not file_list, "List of files should be empty for an empty folder.")

    def test_edge_case_irrelevant_file_types(self):
        """
        Tests that the function ignores non-text files in a folder and returns an empty list
        when no text files are present.
        """
        irrelevant_folder = os.path.join(self.test_dir, 'irrelevant_files')
        os.makedirs(irrelevant_folder)
        with open(os.path.join(irrelevant_folder, 'test.csv'), 'w') as f:
            f.write('This is a CSV file.')
        with open(os.path.join(irrelevant_folder, 'test.py'), 'w') as f:
            f.write('print("Hello World")')

        file_list, _ = read_text_files(irrelevant_folder)
        self.assertIsInstance(file_list, list, "The function should return a list.")
        self.assertTrue(not file_list, "List of files should be empty when only irrelevant files are present.")

    def test_edge_case_mixed_file_types(self):
        """
        Tests that the function correctly reads only the text files when a folder contains
        a mix of text and non-text files.
        """
        file_list, _ = read_text_files(self.input_dir)
        self.assertIsInstance(file_list, list, "The function should return a list.")
        self.assertEqual(len(file_list), 2, "List of files should contain exactly 2 strings from the text files.")

        self.assertIn('This is the content of file one.', file_list)
        self.assertIn('And this is the content of file two.', file_list)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)