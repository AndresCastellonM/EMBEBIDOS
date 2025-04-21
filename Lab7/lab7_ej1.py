import cv2
import numpy as np
import math

# 1. Open and resize image to 1000x1000

image = cv2.imread("images.jpeg")
if image is None:
    print("Error: No se pudo cargar la imagen.")
    exit()

resized_1000 = cv2.resize(image, (1000, 1000))
cv2.imshow("Original", image)
cv2.imshow("Resized 1000x1000", resized_1000)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 2. Ask user to choose resize option
scale_options = {
    "small": 0.5,
    "medium": 1.5,
    "big": 2
}

choice = input("Select image size (original, small, medium, big): ").lower()
if choice == "original":
    rescaled = image.copy()
elif choice in scale_options:
    scale = scale_options[choice]
    rescaled = cv2.resize(image, (int(image.shape[1]*scale), int(image.shape[0]*scale)))
else:
    print("Option not recognized. Using original.")
    rescaled = image.copy()

cv2.imshow(f"{choice.capitalize()} size", rescaled)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 3. Rotate image 90° every time a key is pressed
rotated = image.copy()
while True:
    cv2.imshow("Press any key to rotate, ESC to exit", rotated)
    key = cv2.waitKey(0)
    if key == 27:  # ESC
        break
    rotated = cv2.rotate(rotated, cv2.ROTATE_90_CLOCKWISE)
cv2.destroyAllWindows()


def show_quadrants(image):
    n = int(input("Numero de cuadrantes: "))
    # Determinar si se puede formar una cuadrícula cuadrada (2x2, 4x4, etc.)
    root = int(math.sqrt(n))
    if root * root != n:
        print(f"No se puede dividir en cuadrantes iguales con {n} partes. Se ajustará a {(root+1)**2}")
        n = (root + 1) ** 2
        root = root + 1

    height, width = image.shape[:2]
    h_step = height // root
    w_step = width // root

    for i in range(root):
        for j in range(root):
            y1 = i * h_step
            y2 = (i + 1) * h_step
            x1 = j * w_step
            x2 = (j + 1) * w_step
            quadrant = image[y1:y2, x1:x2]
            title = f"Quadrant {i * root + j + 1}"
            cv2.imshow(title, quadrant)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

resized = cv2.resize(image, (800, 800))  # Asegurarse de un tamaño divisible
show_quadrants(resized)

