import cv2
import numpy as np

# Load the video file
cap = cv2.VideoCapture('C:\\Users\Egor\Projects\Speccurs_image_processing\\aging_videos\\recources\\test.mp4')

# Define the output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(
    'C:\\Users\Egor\Projects\Speccurs_image_processing\\aging_videos\\recources\output_test.mp4', 
    fourcc, 
    30.0, 
    (int(cap.get(3)), int(cap.get(4)))
    )

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply a sepia tone to the frame
    frame_sepia = cv2.transform(frame, np.matrix([[0.272, 0.534, 0.131],
                                                  [0.349, 0.686, 0.168],
                                                  [0.393, 0.769, 0.189]]))
    frame_sepia = cv2.convertScaleAbs(frame_sepia)

    # Add noise to the frame
    noise = np.random.normal(0, 25, frame.shape)
    noise_clipped = np.clip(noise, 0, 255).astype(np.uint8)
    frame_noisy = cv2.add(frame_sepia, noise_clipped)    

    # Apply a Gaussian blur to the frame
    frame_blurred = cv2.GaussianBlur(frame_sepia, (5, 5), 0)

    # Add some scratches to the frame
    scratches = np.random.randint(0, 255, frame.shape[:2], dtype=np.uint8)
    scratches = cv2.threshold(scratches, 50, 255, cv2.THRESH_BINARY)[1]
    scratches = cv2.resize(scratches, (frame_blurred.shape[1], frame_blurred.shape[0]))
    
    frame_scratched = cv2.bitwise_and(frame_blurred, frame_blurred, mask=scratches)

    # Write the transformed frame to the output video
    out.write(frame_scratched)

    cv2.imshow('frame', frame_scratched)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()