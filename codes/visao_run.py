import cv2 as cv
import numpy as np

def region_of_interest(image):# divide a imagem horizontalmente
    height = image.shape[0]
    width = image.shape[1]
    polygons = np.array([
        [(0, height), (width, height), (width, height // 2), (0, height // 2)]
    ])
    mask = np.zeros_like(image)  # Criar máscara com as mesmas dimensões da imagem
    cv.fillPoly(mask, polygons, 255)
    masked_image = cv.bitwise_and(image, mask)  # Aplica a máscara corretamente
    return masked_image

def split_image(masked_image):# divide a imagem em direita e esquerda 
    height = masked_image.shape[0]
    width = masked_image.shape[1]
    mid_x = width // 2
    left_mask = np.zeros_like(masked_image)
    left_mask[:, :mid_x-1] = masked_image[:, :mid_x-1]
    
    right_mask = np.zeros_like(masked_image)
    right_mask[:, mid_x+1:] = masked_image[:, mid_x+1:]
    return left_mask, right_mask

def detect_lines(image):
    line_length= 50
    max_gap=5
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 1)
    canny = cv.Canny(blurred, 50, 210)# 50,150
    cropped_left , cropped_right= split_image(canny)
    lines_left = cv.HoughLinesP(cropped_left, 1, np.pi / 180, 50, minLineLength=line_length, maxLineGap=max_gap)
    lines_right = cv.HoughLinesP(cropped_right, 1, np.pi / 180, 50, minLineLength=line_length, maxLineGap=max_gap)
    return cropped_left ,cropped_right,lines_left, lines_right

def draw_lines(image, lines_left, lines_right):
    line_image = np.zeros_like(image)
    if lines_left is not None:
        for line in lines_left:
            x1, y1, x2, y2 = line[0]
            cv.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    combined_image_left = cv.addWeighted(image, 0.8, line_image, 1, 1)

    if lines_right is not None:
        for line in lines_right:
            x1, y1, x2, y2 = line[0]
            cv.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
    combined_image_right = cv.addWeighted(image, 0.8, line_image, 1, 1)
    return combined_image_left,combined_image_right

def main():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Não foi possível capturar o quadro.")
            break

        canny_left,canny_right ,lines_left, lines_right = detect_lines(frame)
        line_image_left , line_image_right= draw_lines(frame, lines_left, lines_right)
        #line_image_right = draw_lines(frame, lines_right)

        cv.imshow('Linhas Direitas', line_image_right)
        cv.imshow('Canny Image', canny_left)
        cv.imshow('Canny Imagem', canny_right)
        

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()

