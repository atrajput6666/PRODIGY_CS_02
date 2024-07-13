from PIL import Image
def encode_image(image_path, secret_message, output_path):
    # Open the input image
    image = Image.open(image_path)
    pixels = image.load()

    # Convert the secret message to a binary string
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    binary_message += '1111111111111110'  # End of message delimiter

    # Get the dimensions of the image
    width, height = image.size

    message_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])

            for i in range(3):  # Loop through the RGB values
                if message_index < len(binary_message):
                    pixel[i] = int(format(pixel[i], '08b')[:-1] + binary_message[message_index], 2)
                    message_index += 1

            pixels[x, y] = tuple(pixel)

            if message_index >= len(binary_message):
                break
        if message_index >= len(binary_message):
            break

    # Save the modified image
    image.save(output_path)

def decode_image(image_path):
    # Open the input image
    image = Image.open(image_path)
    pixels = image.load()

    # Get the dimensions of the image
    width, height = image.size

    binary_message = ''
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]

            for i in range(3):  # Loop through the RGB values
                binary_message += format(pixel[i], '08b')[-1]

    # Convert the binary string to a secret message
    binary_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    secret_message = ''.join(chr(int(char, 2)) for char in binary_message)

    # Find the end of message delimiter
    end_index = secret_message.find('ÿÿÿþ')
    if end_index != -1:
        secret_message = secret_message[:end_index]

    return secret_message

# Example usage
encode_image('input_image.png', 'Hello, World!', 'encoded_image.png')
decoded_message = decode_image('encoded_image.png')
print('Decoded message:', decoded_message)
