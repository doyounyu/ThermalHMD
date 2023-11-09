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





def main():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()


    # Setting up variables
    mode = 1  # Default mode
    threshold_value = 100  # Manual threshold value


    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        # Get the height of the frame
        height = frame.shape[0]

        # Extract upper half of the frame
        upper_half = frame[:height // 2, :]

        # Convert upper half to grayscale
        gray_upper_half = cv2.cvtColor(upper_half, cv2.COLOR_BGR2GRAY)

        # Compute average brightness of upper_half
        avg_brightness = np.mean(gray_upper_half)

        # If avg_brightness is in the upper 10% of possible values, color upper_half red
        # if gray_upper_half > 0.5 * 255:
        #    upper_half[:, :, 1:3] = 0  # Set G and B channels to 0, keeping R channel

        # Resize the resulting frame before displaying
        scale_percent = 200  # percent of original size, you can change as you need
        width = int(upper_half.shape[1] * scale_percent / 100)
        height = int(upper_half.shape[0] * scale_percent / 100)
        dim = (width, height)

        # Resize image
        frame = cv2.resize(upper_half, dim, interpolation=cv2.INTER_AREA)

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












        # Press 'q' to exit the video window
        if cv2.waitKey(1) == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
