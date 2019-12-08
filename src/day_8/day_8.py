def main():
    with open('input', 'r') as file_txt:
        # replace new line char
        str_ip = file_txt.read().strip()

    width, height = 25, 6
    layer_size = width * height

    # PART-1
    # store min and calc. for layer iterable 
    print(
            min(       
                (
                    (
                        str_ip[i:i + layer_size].count('0'), 
                        str_ip[i:i + layer_size].count('1') * str_ip[i:i + layer_size].count('2')
                    ) for i in range(0, len(str_ip), layer_size)
                ),
                key=lambda x: x[0]
            )[1]
    )

    # PART-2
    # init as size of layer
    decoded_image = [-1 for i in range(0, layer_size)]
    relative_pixel_ptr = 0
    decoded_pixels_count = 0
    for i in range(len(str_ip)):
        relative_pixel_ptr = i % layer_size
        pixel_value = int(str_ip[i])
        # skip already set decoded pixel
        if decoded_image[relative_pixel_ptr] != -1:
            continue

        # skip transparent pixel
        if pixel_value == 2:
            continue
        
        # set black or white pizel
        decoded_image[relative_pixel_ptr] = pixel_value
        decoded_pixels_count += 1
        
        # if all pixels are decoded
        if decoded_pixels_count == len(decoded_image):
            break
    
    # render message
    for j in range(width - 1):
        layer_str = "".join(str(i) for i in decoded_image[j*width:(j+1)*width])
        print(layer_str.replace('0', ' ').replace('1', 'X'))


if __name__ == "__main__":
    main()
