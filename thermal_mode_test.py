import cv2
import numpy as np

# Function to add text on the right corner
def add_text(frame, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    return cv2.putText(frame, text, position, font, 1, (0, 255, 0), 2, cv2.LINE_AA)

# Function to overlay contours with green color
def draw_contours(frame, contours):
    # Draw all contours
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)  # 3 is the thickness
    return frame


# Function to create a mask and overlay with green color
def apply_mask(frame, mask):
    # Create a green image for overlay
    green_overlay = np.zeros_like(frame)
    green_overlay[mask != 0] = (0, 255, 0)
    
    # Combine the green overlay with the original frame
    masked_frame = cv2.bitwise_or(frame, green_overlay)
    
    return masked_frame


# Read the video file
cap = cv2.VideoCapture('test.mp4')
# Assuming 'cap' is your cv2.VideoCapture object
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_fps = cap.get(cv2.CAP_PROP_FPS)  # Slowing down by half

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, output_fps, (frame_width, frame_height))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Setting up variables
mode = 1  # Default mode
threshold_value = 100  # Manual threshold value

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply manual threshold
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on the frame
    contour_frame = draw_contours(frame.copy(), contours)

    # Check which mode is active
    if mode == 1:
        # Display "ORG HOT" and "FULL THERM"
        frame_with_text = add_text(frame.copy(), "GRN HOT", (10, 50))
        frame_with_text = add_text(frame_with_text, "FULL THERM", (frame.shape[1] - 230, 50))
        cv2.imshow('Video', frame_with_text)

    elif mode == 2:
        # Display "ORG HOT" and "OUTLINE" and show contour overlay
        frame_with_text = add_text(contour_frame, "GRN HOT", (10, 50))
        frame_with_text = add_text(frame_with_text, "OUTLINE", (contour_frame.shape[1] - 230, 50))
        cv2.imshow('Video', frame_with_text)

    elif mode == 3:
        # Create a green image for overlay

        # Combine the green overlay with the original frame using a mask
        combined_frame = apply_mask(frame, binary)

        # Display "ORG HOT" and "OVERLAY"
        frame_with_text = add_text(combined_frame, "GRN HOT", (10, 50))
        frame_with_text = add_text(frame_with_text, "OVERLAY", (combined_frame.shape[1] - 230, 50))
        cv2.imshow('Video', frame_with_text)


    out.write(frame_with_text)

    # Check for user input to switch between modes
    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'):
        mode = 1
    elif key == ord('2'):
        mode = 2
    elif key == ord('3'):
        mode = 3
    elif key == ord('q'):
        # Quit if 'q' is pressed
        break

# Release everything when job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
