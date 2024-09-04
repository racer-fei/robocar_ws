import cv2 as cv
import numpy as np

def apply_mask(image, mask):
    """
    Aplica uma máscara à imagem.
    """
    masked_image = cv.bitwise_and(image, image, mask=mask)
    return masked_image

def region_of_interest(image, roi_polygon):
    """
    Aplica uma máscara para focar na região de interesse (ROI) da imagem.
    """
    mask = np.zeros_like(image[:, :, 0])  # Máscara em escala de cinza
    cv.fillPoly(mask, roi_polygon, 255)
    return apply_mask(image, mask)

def detect_edges(image):
    """
    Detecta as bordas da imagem.
    """
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 7)
    equalized = cv.equalizeHist(blurred)
    edges = cv.Canny(equalized, 400, 150)
    return edges

def apply_gabor_filter(image):
    """
    Aplica um filtro de Gabor para realçar as linhas.
    """
    gabor_kernel = cv.getGaborKernel((21, 21), 5, np.pi / 4, 10, 1, 0, ktype=cv.CV_32F)
    filtered_image = cv.filter2D(image, cv.CV_8UC1, gabor_kernel)
    return filtered_image

def detect_lines(image):
    """
    Detecta as linhas da imagem.
    """
    edges = detect_edges(image)
    roi_polygon = np.array([[(0, image.shape[0]), (image.shape[1], image.shape[0]), (image.shape[1], image.shape[0] // 2), (0, image.shape[0] // 2)]])
    cropped_edges = region_of_interest(edges, roi_polygon)
    lines = apply_gabor_filter(cropped_edges)
    return lines

def draw_lines(image, lines):
    """
    Desenha as linhas detectadas sobre a imagem original.
    """
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if len(line) == 4:
                x1, y1, x2, y2 = line
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

        lines = detect_lines(frame)
        line_image = draw_lines(frame, lines)

        cv.imshow('Detectando linhas', line_image)
        cv.imshow('Edges', lines)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__== '__main__':
    main()
