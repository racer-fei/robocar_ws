import cv2 as cv
import numpy as np

def region_of_interest(image):
    """
    Aplica uma máscara para focar na região de interesse (ROI) da estrada, que é tipicamente a metade inferior da imagem.
    """
    height = image.shape[0]
    polygons = np.array([
        [(0, height), (image.shape[1], height), (image.shape[1], height // 2), (0, height // 2)]
    ])
    mask = np.zeros_like(image[:, :, 0])  # Máscara agora é uma imagem em escala de cinza
    cv.fillPoly(mask, polygons, 255)
    masked_image = cv.bitwise_and(image, image, mask=mask)  # Aplica a máscara corretamente
    return masked_image

def detect_lines(image):
    """
    """
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 7)
    equaliza = cv.equalizeHist(gray)
    canny = cv.Canny(equaliza, 400, 150)
    cropped_edges = region_of_interest(canny)
    gabor = cv.getGaborKernel((21, 21), 5, np.pi / 4, 10, 1, 0, ktype=cv.CV_32F)
    #lines = cv.filter2D(cropped_edges, cv.CV_8UC1, gabor)  # Corrige o tipo da imagem filtrada
    #lines = cv.HoughLinesP(cropped_edges, 1, np.pi / 180, 150, minLineLength=50, maxLineGap=50)  # Detecta linhas
    return canny, lines  # Retorna o resultado da detecção de linhas

def draw_lines(image, lines):
    """
    """
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if len(line[0]) == 4:
                x1, y1, x2, y2 = line[0]
                cv.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    combined_image = cv.addWeighted(image, 0.8, line_image, 1, 1)
    return combined_image

def main():
    """
    Função principal para abrir a câmera e detectar linhas de rodovia em tempo real.
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

        canny_image, lines = detect_lines(frame)
        line_image = draw_lines(frame, lines)

        cv.imshow('Detectando linhas', line_image)
        cv.imshow('Canny Image', canny_image)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
