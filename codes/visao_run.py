#GPT

import cv2 as cv
import numpy as np

def crop_left_half(frame):
    """Corta a imagem verticalmente ao meio e utiliza somente o lado esquerdo."""
    height, width = frame.shape[:2]
    return frame[:, :width // 2]

def roi_bottom_half(frame):
    """Corta a imagem horizontalmente ao meio e utiliza somente a metade inferior."""
    height, width = frame.shape[:2]
    return frame[height // 2:, :]

def calculate_angle(x1, y1, x2, y2):
    """Calcula o ângulo da linha com base nas coordenadas dos pontos."""
    delta_y = y2 - y1
    delta_x = x2 - x1
    angle = np.degrees(np.arctan2(delta_y, delta_x))
    return angle

def process_frame(frame):

    frame = crop_left_half(frame)
    frame = roi_bottom_half(frame)

    # Preprocessing for robust line detection
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (7, 7), 0)  # Adjust blur size as needed
    edges = cv.Canny(blurred, 50, 150)  # Adjust thresholds based on lighting

    # Morphological operations for noise reduction and line thinning
    kernel = np.ones((3, 3), np.uint8)
    edges = cv.dilate(edges, kernel, iterations=1)
    edges = cv.erode(edges, kernel, iterations=1)

    length = 100  # Adjust minimum line length based on image size
    gap = 5       # Adjust maximum gap between line segments

    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=length, maxLineGap=gap)

    if lines is not None:
        left_lines = []
        right_lines = []

        # Filter lines based on angle and position for lane detection
        for x1, y1, x2, y2 in lines[:, 0]:
            angle = calculate_angle(x1, y1, x2, y2)

            if abs(angle) > 5:  # Ignore near-horizontal lines
                if x1 < frame.shape[1] // 2:  # Line on the left side
                    left_lines.append((x1, y1, x2, y2))
                else:  # Line on the right side
                    right_lines.append((x1, y1, x2, y2))

            # Draw detected lines for visualization (optional)
            cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Calculate lane center
        if left_lines and right_lines:
            left_center = np.mean([x1 for x1, _, _, _ in left_lines])
            right_center = np.mean([x2 for _, _, x2, _ in right_lines])

            if left_center is not None and right_center is not None:
                center_line = (left_center + right_center) / 2
                cv.line(frame, (int(center_line), 0), (int(center_line), frame.shape[0]), (255, 0, 0), 2)

                # Calculate navigation error (distance from center)
                error = center_line - (frame.shape[1] / 2)
                print(f"Erro de navegação (distância do centro da pista): {error}")

                # **A* Integration (example):**
                # Assume A* takes `center_line` (distance from image center) as input.
                # You can further process `error` or `center_line` for A*.
                # Astar_object.update(center_line)  # Replace with your A* implementation

    return frame



def main():
    cap = cv.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_frame(frame)

        cv.imshow('Pista', processed_frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
