import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
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
        resized = cv2.resize(upper_half, dim, interpolation=cv2.INTER_AREA)

        # Display the resulting frame
        cv2.imshow('Rainbow Video', resized)

        # Press 'q' to exit the video window
        if cv2.waitKey(1) == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
