def file_read(input_file_path) -> bytes:
    with open(input_file_path, 'rb') as file:
        text = file.read()
    return text

def file_write(input_file_path, text):
    with open(input_file_path, 'wb') as file:
        file.write(text)

