import cv2
import numpy as np
import random

# Define color ranges with different variable names
color_bounds = {
    'RED': (np.array([160, 100, 100]), np.array([180, 255, 255])),
    'GREEN': (np.array([40, 70, 70]), np.array([80, 255, 255])),
    'BLUE': (np.array([100, 150, 0]), np.array([140, 255, 255]))
}

# Initialize the camera
video_source = cv2.VideoCapture(0)

def calculate_confidence(contour, color_hsv, color_name):
    # Calculate the area of the contour
    area = cv2.contourArea(contour)
    
    # Calculate the color purity based on the distance from the color bounds
    lower_bound, upper_bound = color_bounds[color_name]
    color_purity = 1.0 - np.linalg.norm(color_hsv - np.mean(lower_bound, axis=0)) / np.linalg.norm(upper_bound - lower_bound)
    
    # Combine area and color purity to get the confidence score
    confidence = area * color_purity
    return confidence

def detect_laser_pointers(frame):
    converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for color_name, (lower_bound, upper_bound) in color_bounds.items():
        mask = cv2.inRange(converted_frame, lower_bound, upper_bound)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        blurred_mask = cv2.GaussianBlur(mask, (15, 15), 0)
        contours, _ = cv2.findContours(blurred_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 50:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                distance = 200 / (radius + 1)
                
                # Calculate the confidence of the detection
                color_hsv = np.mean(converted_frame[int(y):int(y)+radius, int(x):int(x)+radius], axis=(0, 1))
                confidence = calculate_confidence(contour, color_hsv, color_name)
                if confidence < 500: 
                    continue
                
                if color_name == 'RED': 
                    colorr = (0,0,255)
                if color_name == 'GREEN': 
                    colorr = (0,255,0)
                if color_name == 'BLUE': 
                    colorr = (255,0,0)
                text = f"{color_name} Laser\n Distance: {distance:.2f} cm,\n Confidence: {confidence:.2f}"
                
                # Introduce a random offset for the text position
                text_offset = (random.randint(-10, 10), random.randint(-10, 10))
                cv2.circle(frame, center, radius, colorr, 2)
                cv2.putText(frame, text, (center[0] + text_offset[0], center[1] + text_offset[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, colorr, 2)

while True:
    ret, frame = video_source.read()
    if not ret:
        break
    
    detect_laser_pointers(frame)
    
    cv2.imshow("Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_source.release()
cv2.destroyAllWindows()
