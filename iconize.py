import cv2
import numpy as np

palette = np.array([
    [0, 0, 0],        # black
    [128, 0, 0],      # maroon
    [0, 128, 0],      # green
    [128, 128, 0],    # olive
    [0, 0, 128],      # navy
    [128, 0, 128],    # purple
    [0, 128, 128],    # teal
    [192, 192, 192],  # silver
    [128, 128, 128],  # gray
    [255, 0, 0],      # red
    [0, 255, 0],      # lime
    [255, 255, 0],    # yellow
    [0, 0, 255],      # blue
    [255, 0, 255],    # fuchsia
    [0, 255, 255],    # aqua
    [255, 255, 255]   # white
], dtype=np.uint8)

image_path = input("image path: ")
image = cv2.imread(image_path)

image_size_input = input("Input icon size (default: 64): ")
image_size = int(image_size_input) if image_size_input else 64

method_input = input("linear or euclidean interpolation (l/e): ")

if image is None:
    print("Error: Could not load the image.")
else:
    reduced_image = cv2.resize(image, (image_size, image_size))

    def find_closest_color_euclidean(pixel, palette):
        pixel = np.float32(pixel)  
        palette = np.float32(palette) 
        distances = np.sqrt(np.sum((palette - pixel) ** 2, axis=1))
        closest_index = np.argmin(distances)
        return palette[closest_index]

    def find_closest_color_linear(pixel, palette):
        pixel = np.float32(pixel)
        palette = np.float32(palette)
        differences = np.abs(palette - pixel)
        linear_diffs = np.sum(differences, axis=1)
        closest_index = np.argmin(linear_diffs)
        return palette[closest_index]

    pixels = reduced_image.reshape((-1, 3))

    if method_input.lower() == 'e':
        quantized_pixels = np.array([find_closest_color_euclidean(pixel, palette) for pixel in pixels], dtype=np.uint8)
    else:
        quantized_pixels = np.array([find_closest_color_linear(pixel, palette) for pixel in pixels], dtype=np.uint8)

    quantized_image = quantized_pixels.reshape(reduced_image.shape)

    save_path = 'icon_'
    if method_input.lower() == 'e':
        save_path += 'euclidean.png'
    else:
        save_path += 'linear.png'
    cv2.imwrite(save_path, quantized_image)

    print(f"Image saved successfully as {save_path}")
