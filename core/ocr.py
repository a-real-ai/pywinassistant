import pyautogui
import win32gui
import win32process
import psutil
from PIL import ImageGrab
import re
from fuzzywuzzy import fuzz
from concurrent.futures import ThreadPoolExecutor
import math
# Function to preprocess the image for better OCR results
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pytesseract
import pygetwindow as gw

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to calculate similarity using fuzzywuzzy
def calculate_similarity(input_string, match_string):
    # Calculate basic similarity score using partial_ratio
    basic_similarity = fuzz.partial_ratio(input_string.lower(), match_string.lower())

    # Adjust score based on the length difference
    length_difference = len(input_string) - len(match_string)

    # If the match string is shorter than the input string, reduce the score
    if length_difference > 0:
        # For example, reduce the score by 5 points for each missing character
        score_penalty = 50 * length_difference
        adjusted_score = max(basic_similarity - score_penalty, 0)  # Ensure the score doesn't go below 0
    else:
        # If the match string is not shorter, no penalty is applied
        adjusted_score = basic_similarity

    return adjusted_score

# New function for multi-processing
def parallel_ocr(data):
    x, y, w, h = data
    cropped_image = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    processed_images = preprocess_image(
        cropped_image,
        contrast_levels=[128, 152],
        invert=True,
        scales=[1, 1.25]
    )

    results = []
    for img in processed_images:
        text = pytesseract.image_to_string(img)
        if text:
            results.append(text)

    results.sort(key=len, reverse=True)
    return results[0] if results else ""


# Add your WindowClassifier class definition here
def get_focused_window_details():
    try:
        # Get the handle of the currently focused window
        window_handle = win32gui.GetForegroundWindow()

        # Get window text (title)
        window_title = win32gui.GetWindowText(window_handle)

        # Get the process ID of the window
        _, window_pid = win32process.GetWindowThreadProcessId(window_handle)

        # Get the process name from the process ID
        process = psutil.Process(window_pid)
        process_name = process.name()

        # Get window size and position
        rect = win32gui.GetWindowRect(window_handle)
        window_position = (rect[0], rect[1])
        window_size = (rect[2] - rect[0], rect[3] - rect[1])

        return window_title, window_handle, window_pid, process_name, window_position, window_size
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None, None, None, None, None  # Return None for all values in case of an exception

    pass

def ocr_image(image):
    # Apply preprocessing with filters directly in the OCR function
    text = ocr_image_with_filters(image)
    return text

def preprocess_image(
    image,
    grayscale=True,
    invert=False,
    contrast_levels=None,
    scales=None,
    use_threshold=False,
    gaussian_blur_radius=None,
    median_filter_size=None,
    bilateral_filter_params=None,
    sharpen=False,
    edge_enhance=False,
    contrast_enhance_factor=1.0
):
    # Initialize default values if none provided
    if scales is None:
        scales = [1]  # Default scale is 100%
    if contrast_levels is None:
        contrast_levels = [128]  # Default threshold for binarization

    processed_images = []

    for scale in scales:
        # Resize image if scale is not 1
        if scale != 1:
            resized_image = image.resize((int(image.width * scale), int(image.height * scale)), Image.ANTIALIAS)
        else:
            resized_image = image

        if grayscale:
            # Convert image to grayscale
            processed_image = resized_image.convert('L')
        else:
            processed_image = resized_image

        if invert:
            # Invert image colors
            processed_image = ImageOps.invert(processed_image)

        if sharpen:
            # Apply sharpen filter
            processed_image = processed_image.filter(ImageFilter.SHARPEN)

        if edge_enhance:
            # Enhance the edges in the image
            processed_image = processed_image.filter(ImageFilter.EDGE_ENHANCE)

        if contrast_enhance_factor != 1.0:
            # Enhance the contrast of the image
            enhancer = ImageEnhance.Contrast(processed_image)
            processed_image = enhancer.enhance(contrast_enhance_factor)

        if gaussian_blur_radius:
            # Apply Gaussian Blur
            processed_image = processed_image.filter(ImageFilter.GaussianBlur(gaussian_blur_radius))

        if median_filter_size:
            # Apply Median Filter
            processed_image = processed_image.filter(ImageFilter.MedianFilter(median_filter_size))

        if bilateral_filter_params:
            # Apply Bilateral Filter
            diameter, sigma_color, sigma_space = bilateral_filter_params
            processed_image = processed_image.filter(ImageFilter.BilateralFilter(diameter, sigma_color, sigma_space))

        if use_threshold:
            # Apply threshold to binarize the image
            thresholded_image = processed_image.point(lambda x: 0 if x < contrast_levels[0] else 128, '1')
            processed_images.append(thresholded_image)
        else:
            # If not using threshold, just append the processed image
            processed_images.append(processed_image)

    return processed_images

def ocr_image_with_filters(image):
    # Apply preprocessing with filters
    preprocessed_images = preprocess_image(
        image,
        grayscale=True,
        invert=False,
        contrast_levels=[128],
        scales=[1],
        use_threshold=True,
        gaussian_blur_radius=None,
        median_filter_size=None,
        bilateral_filter_params=None,
        sharpen=True,
        edge_enhance=False,
        contrast_enhance_factor=2.0
    )

    # Since preprocess_image returns a list, we take the first (and should be only) image
    preprocessed_image = preprocessed_images[0]

    # Display the modified image DEBUGGING.
    # preprocessed_image.show()

    # Perform OCR on the preprocessed image
    text = pytesseract.image_to_string(preprocessed_image)

    # print(f"IMAGE PROCESSED:\n{text}")
    return text.strip()


def click_best_match(best_match):
    if best_match:
        # Calculate the center of the bounding box
        center_x = best_match['x'] + best_match['w'] // 2
        center_y = best_match['y'] + best_match['h'] // 2

        # Perform the click action using pyautogui
        pyautogui.moveTo(center_x, center_y, 0.5, pyautogui.easeOutQuad)
        pyautogui.click(center_x, center_y)
        return f"Clicked on the best match: '{best_match['text']}' at position: ({center_x}, {center_y})"
    else:
        return "No suitable matches to click on the screen."


# Function to compute the distance between two points for proximity scoring.
def distance_between(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
# Enhance this function to score matches not only based on OCR confidence and text similarity but also their proximity.
def score_and_rank_matches(matches):
    for i, match in enumerate(matches):
        for other_match in matches[i+1:]:
            proximity = 1000 / (distance_between(match['position'], other_match['position']) + 1)  # Simple proximity score
            match['score'] += proximity
            other_match['score'] += proximity
    matches.sort(key=lambda x: x['score'], reverse=True)  # Sort matches based on the score
    return matches


# Update click_best_match to intelligently click between close matches if found
def click_best_matches(coincidences):
    if not coincidences:
        return "No suitable matches to click on the screen."
        # Filter out negative-scored matches
    positive_score_matches = [match for match in coincidences if match['score'] > 0]

    if not positive_score_matches:
        return "No matches with a positive score to click on the screen."

    # Calculate the average position (centroid) in case of close matches
    if len(coincidences) > 1:
        average_x = sum(match['center'][0] for match in coincidences) // len(coincidences)
        average_y = sum(match['center'][1] for match in coincidences) // len(coincidences)
        pyautogui.click(average_x, average_y)
        return f"Clicked on the average position: ({average_x}, {average_y})"
    else:
        best_match = coincidences[0]
        center_x = best_match['center'][0]
        center_y = best_match['center'][1]

        pyautogui.click(center_x, center_y)
        return f"Clicked on the best match: '{best_match['text']}' at position: ({center_x}, {center_y})"

# Function to execute best_match_with_proximity in parallel and find the most probable click position
def find_best_match_with_proximity(input_string, within_window=False):
    if within_window:
        _, _, _, _, window_position, window_size, _, _ = get_focused_window_details()
        screenshot = ImageGrab.grab(bbox=(
            window_position[0], window_position[1],
            window_position[0] + window_size[0],
            window_position[1] + window_size[1]))
    else:
        screenshot = ImageGrab.grab()
    d = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
    input_string = input_string.lower()
    input_parts = re.findall(r'\w+|\W+', input_string)  # Split input_string into words and non-alphabetic parts

    coincidences = []  # List to store all matches


    for i in range(len(d['text'])):
        extracted_text = d['text'][i].lower().strip()


        # Skip single and double letters or empty strings
        if len(extracted_text) <= 2 or not extracted_text:
            continue

        score = score = int(d['conf'][i])
        for part in input_parts:
            if part in extracted_text:
                score += 50 if part.isalpha() else 75  # Higher score for non-alphabetic parts


          # Initialize score with OCR confidence

        # Check for literal exact match and score it more points
        if extracted_text == input_string:
            score += 500  # Assign significant points for a literal exact match

        # Use fuzzywuzzy to measure similarity and adjust the score
        similarity_score = fuzz.partial_ratio(input_string, extracted_text)
        if similarity_score > 60:
            score += similarity_score  # Add similarity score to the existing score

        # Penalize score if similarity is low
        if similarity_score < 80:
            score -= 200  # Deduct points if there's low similarity
        # Inside find_best_match_with_proximity
        coincidence = {
            'text': d['text'][i],
            'x': d['left'][i],
            'y': d['top'][i],
            'w': d['width'][i],
            'h': d['height'][i],
            'conf': d['conf'][i],
            'score': score,  # Ensure there is a comma here
            # Add the 'center' key to store the center coordinates of the match
            'center': (d['left'][i] + d['width'][i] // 2, d['top'][i] + d['height'][i] // 2)
        }
        coincidences.append(coincidence)

    # Now we have all coincidences with scores reflecting exactness and similarity
    # Higher score is better

    if coincidences:
        # Sort matches based on the score
        best_match = max(coincidences, key=lambda x: x['score'])
        #################################################
        # print(f"Best match: '{best_match['text']}' with score {best_match['score']}")
        return best_match
    else:
        print("No matches found.")
        return None

# Adjusted ocr_focused_window function
def ocr_focused_window():
    # Get details of the focused window
    _, _, _, _, window_position, window_size, _, _ = get_focused_window_details()
    # Capture only the area of the focused window
    screenshot = ImageGrab.grab(bbox=(
    window_position[0], window_position[1], window_position[0] + window_size[0], window_position[1] + window_size[1]))
    # Perform OCR with preprocessing and filtering
    text = ocr_image_with_filters(screenshot)
    return text


# Adjusted ocr_screen function
def ocr_screen(focused=False):
    if focused:
        # Get the focused window
        window = gw.getActiveWindow()
        if window is not None:
            # Get the position of the focused window
            x, y, width, height = window.left, window.top, window.width, window.height
            # Capture the focused window
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
        else:
            # Fallback in case no window is focused
            screenshot = ImageGrab.grab()
    else:
        # Get a screenshot of the entire screen
        screenshot = ImageGrab.grab()

    # Perform OCR with preprocessing and filtering (assuming this is a function you have)
    text = ocr_image_with_filters(screenshot)
    return text


def find_probable_click_position(input_string, attempts=30):
    print(f"Finding the most probable click position for \"{input_string}\"...")
    with ThreadPoolExecutor(max_workers=attempts) as executor:
        print(f"Running {attempts} attempts in parallel...")
        # Run the function multiple times in parallel
        futures = [executor.submit(find_best_match_with_proximity, input_string) for _ in range(attempts)]
        print(f"Waiting for {attempts} parallel attempts to finish...")

        # Collect results, filtering out those with a non-positive score
        results = [future.result() for future in futures if future.result() is not None and future.result()['score'] > 0]
        print(f"Found {len(results)} matches with a positive score.")
        print("Scoring and ranking matches based on proximity...")
    print(f"Found {len(results)} matches with a positive score.")
    # Find the most probable best match based on the score
    if results:
        most_probable_match = max(results, key=lambda match: match['score'])
        return most_probable_match
    return None

# Main execution block
if __name__ == "__main__":
    input_string = "Neon Genesis Evangelion"  # Example input string
    most_probable_match = find_probable_click_position(input_string)

    # Provide feedback and click action based on most probable match
    if most_probable_match:
        click_result = click_best_matches([most_probable_match])
        print(f"Most probable match \"{most_probable_match['text']}\" Located at \"x={most_probable_match['center'][0]}, y={most_probable_match['center'][1]}\" with score {most_probable_match['score']}")

    else:
        print("No suitable matches found on screen for the input string.")