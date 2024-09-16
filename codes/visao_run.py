import cv2
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
    # Pré-processamento: cortar a imagem verticalmente ao meio e usar somente o lado esquerdo
    frame = crop_left_half(frame)
    
    # Pré-processamento: cortar a imagem horizontalmente ao meio e usar somente a metade inferior
    frame = roi_bottom_half(frame)
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar um desfoque para reduzir o ruído
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detecção de bordas usando o Canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # Encontrar linhas usando a Transformada de Hough Probabilística
    length = 100
    gap = 9
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=length, maxLineGap=gap)
    
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            # Calcular ângulo da linha
            angle = calculate_angle(x1, y1, x2, y2)
            
            # Ignorar linhas horizontais (ângulo próximo de 0 graus)
            if abs(angle) > 5:  # Ajuste o valor conforme necessário
                # Desenhar as linhas na imagem original
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Mostrar o ângulo da linha (ignorado se for horizontal)
                print(f"Angulo da linha: {angle:.2f} graus")
                
                # Aqui você pode adicionar a lógica para controlar os motores com base no ângulo
            else:
                print("Linha horizontal detectada e ignorada.")
    
    return frame

def main():
    # Abrir a captura de vídeo (0 para a webcam padrão)
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Processar o frame
        processed_frame = process_frame(frame)
        
        # Mostrar o frame processado
        cv2.imshow('Pista', processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
