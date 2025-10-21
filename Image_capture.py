import cv2
import numpy as np
# Open the webcam
cap = cv2.VideoCapture(0)

# Set a directory where you want to save the captured frames
save_directory = r"C:\Users\SSSARC-I7-08\Desktop\Raw Data/"

# Initialize a counter for indexing
frame_counter = 1

# Set constant black window size
window_size = (400, 70)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Create a black window
    saturation_display = np.zeros((window_size[1], window_size[0], 3), dtype=np.uint8)

    # Check saturation status
    max_pixel_value = frame.max()
    saturation_status = "Saturated!!!" if max_pixel_value > 254 else "Under Saturation Level"
    # Set font color based on saturation status
    font_color = (0, 0, 255) if max_pixel_value > 254 else (0, 255, 0)

    # Display the saturation status in the black window
    cv2.putText(saturation_display, saturation_status, (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 2)
    cv2.imshow('Saturation Status', saturation_display)

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Wait for the 's' key to be pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Save the current frame as an image
        save_path = f"{save_directory}Image_{frame_counter}.jpg"
        cv2.imwrite(save_path, frame)
        print(f"Saved Image_{frame_counter}.jpg - {saturation_status}")
        frame_counter += 1
    elif key == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
