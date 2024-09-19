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
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blurred, 50, 150)
    length = 110
    gap = 9
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=length, maxLineGap=gap)
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            angle = calculate_angle(x1, y1, x2, y2)
            
            if abs(angle) > 5:  
                # Desenhar as linhas na imagem original
                cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
 
                print(f"Angulo da linha: {angle:.2f} graus")
            else:
                print("Linha horizontal detectada e ignorada.")
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
