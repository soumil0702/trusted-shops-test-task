import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class EndToEndTests(unittest.TestCase):
    def setUp(self):
        # Create a ChromeDriver instance, passing the Service object
        self.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()))
        self.driver.maximize_window()

        # Setting a wait variable to use later for explicit waits
        self.wait = WebDriverWait(self.driver, 10)
        test_url = "https://www.trustedshops.de/bewertung/info_X77B11C1B8A5ABA16DDEC0C30E7996C21.html"
        
        # Navigate to the webpage you want to test
        self.driver.get(test_url)

    def tearDown(self):
        # Clean up after each test case
        self.driver.quit()

    def test_title(self):
        title_check = ""
        
        # Compare the variable title_check against the actual title to see if it exists, if empty an assertion is shown
        self.assertNotEqual(title_check, self.driver.title, "Title is Empty!")

    def test_grade_visible(self):
        # Using XPath since the class name seems dynamically hashed, and may change and therefore fail our test
        element_xpath = '//*[@id="top"]/div/div[4]/div[2]/div[1]/div[1]/div[2]/span'
        grade = self.wait.until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
        self.assertTrue(grade.is_displayed(), "The element is NOT visible")

        # Convert german numbering format to the standard by replacing "," with "."
        text = grade.text.replace(',', '.')
        # Typecast string to a float
        val = float(text)

        # Assertion to check if value >0
        self.assertGreater(val, 0, f"The element value '{val}' is not greater than zero")

    def test_window_text_visible(self):
        # Test to check if the window text is visible and correct when the link is clicked

        # NOTE that you can click on the link with both the link_text or by the XPATH, but the XPATH takes longer even though it's better coding practice, therefore I chose link_text-
        link_text = "Wie berechnet sich die Note?"
        # link_xpath='//*[@id="top"]/div/div[4]/div[2]/div[1]/div[2]/a'
        link = self.driver.find_element(By.LINK_TEXT, link_text)
        # link=self.driver.find_element(By.XPATH,link_xpath)
        link.click()
      
        # Check if popup window exists and is displayed
        popup_window = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test="modal-dialogue"]')))
        self.assertTrue(popup_window.is_displayed(), "The element is NOT visible")

        # To check if the information is relevant, I just picked the text that is least likely to change and is the most relevant information in this case
        expected_text = """Notenberechnung auf Basis der Sternevergabe
        5.00 - 4.50 Sehr gut
        4.49 - 3.50 Gut
        3.49 - 2.50 Befriedigend
        2.49 - 1.50 Ausreichend
        1.49 - 1.00 Mangelhaft
        """
        # Get rid of the whitespace, \n, and \t
        expected_text = ''.join(expected_text.split())
        popup_window_text = ''.join(popup_window.text.split())

        # Check if the expected text is contained in the entire text in the window, otherwise throw assertion
        self.assertIn(expected_text, popup_window_text, "Relevant text NOT in the Window!")

    def test_filter_two_stars(self):
        # Finding by xpath of the anchor tag that contain the class "bRvmSR". The a[4] selects the 4th anchor tag in the tree, in this case it's the 2 star reviews
        # Note that although the class name seems dynamically hashed, it's the only common identifier for each of the star reviews and was a few seconds faster than using the full xpath
        two_star_btn_xpath = '//div[contains(@class,"bRvmSR")]/a[4]'
        two_star_anchor = self.driver.find_elements(By.XPATH, two_star_btn_xpath)
        
        # Check if the 2 stars anchor tag can be clicked, if for example there are no reviews with 2 stars, this won't be clicked and the test would pass
        if two_star_anchor:
            two_star_anchor[0].click()
            # Wait until all the user reviews are visible
            div_elements = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class,"chcERM")]')))

            # Iterate over each user review in the page and check if the stars are = 2
            for div_element in div_elements:
                # Find elements within the div that match the style condition. In this case, we are looking for the golden color stars
                matching_elements = div_element.find_elements(By.XPATH, ".//*[contains(@style, 'color: rgb(255, 220, 15)')]")
                # Assert that the number of matching elements is exactly 2
                self.assertEqual(len(matching_elements), 2, "Number of Stars for this review is not equal to 2")
        else:
            print("No review with 2 stars exists!")

    def test_sum_star_percentages(self):
        # Find the anchor elements of the stars using XPath
        star_percent_elements = self.driver.find_elements(By.XPATH, '//*[@id="top"]/div/div[4]/div[2]/div[2]/div[1]/a/div[3]/span[1]')
        # Initialize a variable to hold the sum of the percentage values
        sum_of_percent = 0
       
        # Iterate over the anchor elements because each anchor element has the span which we can use to extract the percentage of users for each rating
        for star_percent_element in star_percent_elements:
            # Get the text of the span element and convert it to an integer
            # Clean the text such that any "<" or ">" symbols are removed from the text
            cleaned_text = star_percent_element.text.replace(">", "").replace("<", "").strip()
            star_percent_value = int(cleaned_text)
            # Accumulate star percent value to the sum
            sum_of_percent += star_percent_value

        # Perform the assertion to check if the sum is less than 100
        self.assertLessEqual(sum_of_percent, 100, f"Sum of spans ({sum_of_percent}) is not less than 100")


if __name__ == '__main__':
    unittest.main()
