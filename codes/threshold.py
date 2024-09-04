import cv2 as cv
import numpy as np

def detect_lines(image):
    """
    Detecta as linhas na imagem usando a Transformada de Hough.
    """
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, -2)
    blurred = cv.GaussianBlur(gray, (5, 5), 5)
    equaliza = cv.equalizeHist(blurred)
    canny = cv.Canny(equaliza, 50, 150)  # Aplicar Canny
    lines = cv.HoughLinesP(canny, 1, np.pi/180, 150, minLineLength=100, maxLineGap=25)
    return  blurred,equaliza, canny,lines

def draw_lines(image, lines):
    """
    Desenha as linhas detectadas na imagem.
    """
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    combined_image = cv.addWeighted(image, 0.8, line_image, 1, 1)
    return combined_image

def main():
    """
    Função principal para abrir a câmera e detectar linhas em tempo real.
    """
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Não foi possível capturar o quadro.")
            break

        # Corrigido para desempacotar corretamente os quatro valores retornados
        blurred_image,  equaliza_image, canny_image,lines = detect_lines(frame)
        line_image = draw_lines(frame, lines)

        # Corrigido para exibir as imagens corretas
        cv.imshow('Blurred Image', blurred_image)
        cv.imshow('Equaliza Image', equaliza_image)
        cv.imshow('Canny Image', canny_image)
        cv.imshow('Detected Lines', line_image)

        # Sair do loop quando 'q' for pressionado
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
