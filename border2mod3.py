import cv2
import numpy as np

def extract_inside_border(beaker_image_path, border_image_path):
    # Read the images
    beaker_img = cv2.imread(beaker_image_path)
    border_img = cv2.imread(border_image_path, 0)  # Read border image in grayscale

    # Convert border image to binary
    _, border_binary = cv2.threshold(border_img, 240, 255, cv2.THRESH_BINARY)

    # Find contours of the border
    contours, _ = cv2.findContours(border_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    border_contour = max(contours, key=cv2.contourArea)

    # Create a mask for the border
    mask = np.zeros_like(beaker_img)
    cv2.drawContours(mask, [border_contour], -1, (255, 255, 255), -1)

    # Mask the beaker image with the border
    masked_beaker = cv2.bitwise_and(beaker_img, mask)

    # Convert masked beaker image to grayscale
    gray_beaker = cv2.cvtColor(masked_beaker, cv2.COLOR_BGR2GRAY)

    # Find intensity profile along the central vertical line
    central_vertical_line_x = gray_beaker.shape[1] // 2
    intensity_profile = gray_beaker[:, central_vertical_line_x]

    # Find the intensity change along the profile
    intensity_diff = np.diff(intensity_profile)

    # Find the index of maximum intensity change
    max_change_idx = np.argmax(intensity_diff)

    # Use a suitable horizontal line in the lower 50% of the image
    suitable_horizontal_line_y = max_change_idx + gray_beaker.shape[0] // 2

    # Extract liquid surface based on the suitable horizontal line
    liquid_surface_img = masked_beaker.copy()
    cv2.line(liquid_surface_img, (0, suitable_horizontal_line_y), (masked_beaker.shape[1], suitable_horizontal_line_y), (0, 0, 255), 2)

    # Calculate the height of the line from the bottom
    line_height_from_bottom = masked_beaker.shape[0] - suitable_horizontal_line_y

    # Calculate the ratio of the height of the line from the bottom to the height of the border image in percentage
    ratio_percentage = (line_height_from_bottom / masked_beaker.shape[0]) * 100

    return ratio_percentage, liquid_surface_img

# Test the function
beaker_image_path = 'IMG_2860.JPG'
border_image_path = 'IMG_2860_BORDERS.tif'
ratio, result_image = extract_inside_border(beaker_image_path, border_image_path)

# Display results
cv2.imshow('Result', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Display the ratio
print("Ratio of the height of the line from the bottom to the height of the border image in percentage:", ratio)
