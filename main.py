"""
this module can calculate how much fertilizer need given field
by image from satellite
"""
from PIL import Image


def read_files(path, path_20_meter):
    """
    read picture and it's scale from given images
    path - path to field image
    path_20_meter - path to image with line in this scale with length 20m
    """
    meters_20_px = Image.open(path_20_meter).size[0]  # width of image
    size_1px = 20 / meters_20_px

    image_rgb = Image.open(path).convert('RGB')
    image_list = list(image_rgb.getdata())
    width, height = image_rgb.size
    image = []
    for line in range(height):
        image.append(image_list[line*width:(line+1)*width])
    del image_rgb, image_list, width, height
    return image, size_1px ** 2


def pixel_fertilizer_calculations(red, green, blue, size_1px_squared):
    """
    function which calculate how much fertilizer need this pixel of field
    by rgb and size of this pixel (scale)
    """
    correct_color_min_green = 100
    correct_color_max_red = 30
    correct_color_max_blue = 30
    if correct_color_min_green > green:
        delta_green = correct_color_min_green - green
    else:
        delta_green = 0

    if correct_color_max_red < red:
        delta_red = red - correct_color_max_red
    else:
        delta_red = 0

    if correct_color_max_blue < blue:
        delta_blue = blue - correct_color_max_blue
    else:
        delta_blue = 0

    fertilizer_1meter_sq = (delta_blue+delta_red)*0.00025 + delta_green*0.00075
    return fertilizer_1meter_sq * size_1px_squared


def field_fertilizer_calculations(image, size_1px_sq):
    """
    function finally calculate how much fertilizer need field
    work using double integrating
    """
    summary_fertilizer = 0
    for line in image:
        for pixel in line:
            summary_fertilizer += pixel_fertilizer_calculations(*pixel, size_1px_sq)
    return summary_fertilizer


def main():
    """
    main function which do calculating and print results
    """
    image, size_px_sq = read_files(path='field.png',
                                   path_20_meter='20_meters.png')
    fertilizer_mass = field_fertilizer_calculations(image, size_px_sq)
    area = len(image) * len(image[0]) * size_px_sq
    poor_condition_fertilizer = area * 0.03
    if poor_condition_fertilizer < fertilizer_mass:
        print('This field is in poor condition!')
    else:
        print('This field is in good condition!')
    print(f'Area of this field is {round(area,1)} m^2\n'
          f'It need {round(fertilizer_mass, 1)}kg of potassium sulfate.')


if __name__ == '__main__':
    main()
