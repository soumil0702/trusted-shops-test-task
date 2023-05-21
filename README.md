# Automated Testing with Selenium and Python
This directory contains automated tests using Selenium and Python. The tests are designed to run end-to-end tests on a specific webpage from Trustedshops and validate various elements on the page.

## Getting Started
To get started with running the tests, please follow the instructions below:

### Prerequisites
- Python 3.x
- Chrome Browser installed in its standard location (used by the chromedriver in the code)

## Installation
1. Download the required folder containing the test script
2. Open a terminal / cmd on the downloaded folder
3. Install the required Python packages:
```shell
   pip install -r requirements.txt
```
## Running the Tests
To run the automated tests, navigate to the folder where your script is and execute the following command in the cmd/terminal:

```shell
pytest test_suite.py --html=report.html
```
The cmd window should show the test execution results, and a report.html file is
generated in your test folder, which documents the status of each test
(Note you can also execute the script normally but pytest offers the option to generate a
report file which is why i prefer it)
## Test Cases

The automated tests include the following test cases:

- `test_title()`: Checks if the page title is empty.
- `test_grade_visible()`: Verifies if the grade element is visible and its value is greater than zero.
- `test_window_text_visible()`: Tests the visibility of a popup window and checks if the expected text is present.
- `test_filter_two_stars()`: Clicks on a button and verifies if there are filtered reviews with exactly two stars.
- `test_sum_star_percentages()`: Calculates the sum of star percentages and checks if it is less than or equal to 100.

