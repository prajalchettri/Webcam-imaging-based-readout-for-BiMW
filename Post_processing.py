import cv2
import numpy as np
import os

# Function to calculate the sum of pixel values within the ROI
def calculate_roi_sum(roi):
    return np.sum(roi)

# Function to update the ROI information in the same window
def update_roi_info(roi_info_window, roi_x, roi_y, roi_width, roi_height):
    roi_info_window.fill(0)
    info_x = f"ROI X: {roi_x}, ROI Y: {roi_y}"
    info_wh = f"ROI Width: {roi_width}, ROI Height: {roi_height}"
    cv2.putText(roi_info_window, info_x, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(roi_info_window, info_wh, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# Initialize some variables
roi_x, roi_y, roi_width, roi_height = 100, 100, 50, 50  # Initial ROI position and size

image_folder = r'C:/Users/SSSARC-I7-08/Desktop'

# Create a black window to display ROI position and size
roi_info_window = np.zeros((100, 300, 3), dtype=np.uint8)
sum_info_window = np.zeros((100, 300, 3), dtype=np.uint8)

# List to store ROI sum data
roi_sum_data = []

# Load the list of image files in the folder
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(('.jpg', '.png', '.jpeg'))]

if not image_files:
    print("Error: No image files found in the folder.")
else:
    # Load the first image
    first_image = cv2.imread(image_files[0])
    if first_image is None:
        print(f"Error: Could not load the first image {image_files[0]}")
    else:
        while True:
            # Create a copy of the image to avoid overwriting the original image
            display_image = first_image.copy()

            # Draw the ROI on the image
            cv2.rectangle(display_image, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

            # Crop the ROI from the image
            roi = first_image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

            # Calculate the sum of pixel values within the ROI
            roi_sum = calculate_roi_sum(roi)

            # Display the current image
            cv2.imshow('Image with ROI', display_image)

            # Update the ROI info in the same window
            update_roi_info(roi_info_window, roi_x, roi_y, roi_width, roi_height)

            # Display the ROI information in the same window
            cv2.imshow('ROI Info', roi_info_window)

            # Update the sum info window
            sum_info = f'Sum: {roi_sum}'
            sum_info_window.fill(0)
            cv2.putText(sum_info_window, sum_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Display the sum information in a separate window
            cv2.imshow('Sum Info', sum_info_window)

            # Wait for a key event
            key = cv2.waitKey(0)

            if key == ord('w'):  # Move ROI up
                roi_y -= 10
            elif key == ord('s'):  # Move ROI down
                roi_y += 10
            elif key == ord('a'):  # Move ROI left
                roi_x -= 10
            elif key == ord('d'):  # Move ROI right
                roi_x += 10
            elif key == ord('r'):  # Increase ROI size
                roi_width += 10
                roi_height += 10
            elif key == ord('f'):  # Decrease ROI size
                roi_width -= 10
                roi_height -= 10
            elif key == ord('c'):  # Calculate ROI sum for all images
                roi_sum_data = []  # Reset data
                for image_file in image_files:
                    image = cv2.imread(image_file)
                    if image is None:
                        print(f"Error: Could not load the image {image_file}")
                        continue
                    # Crop the ROI from the current image
                    roi = image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
                    # Calculate the sum of pixel values within the ROI
                    roi_sum = calculate_roi_sum(roi)
                    # Display the ROI sum for the current image
                    print(f'Sum for {image_file}: {roi_sum}')
                    roi_sum_data.append((image_file, roi_sum))
            elif key == ord('q'):  # Quit the program
                break

    # Save the ROI sum data to a .txt file
    with open('roi_sum_data.txt', 'w') as file:
        for filename, roi_sum in roi_sum_data:
            file.write(f'{filename}\t{roi_sum}\n')

# Close all OpenCV windows
cv2.destroyAllWindows()
