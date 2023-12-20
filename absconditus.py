import subprocess
import sys

# Intentar importar colorama, instalarlo si no está disponible
try:
    import colorama
    from colorama import Fore, Style
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    import colorama
    from colorama import Fore, Style

colorama.init(autoreset=True)

def box_text(text, padding=1):
    lines = text.split('\n')
    max_width = max(len(line) for line in lines)
    box_width = max_width + 2 * padding

    top_bottom = '+' + '-' * box_width + '+'
    padded_lines = [f"|{' ' * padding}{line}{' ' * (box_width - len(line))}|" for line in lines]

    boxed_text = [top_bottom] + padded_lines + [top_bottom]
    return '\n'.join(boxed_text)

# Mensaje de bienvenida en arte ASCII de d4no :D
welcome_message = """
       __                        ___ __         
 ___ _/ /  ___ _______  ___  ___/ (_) /___ _____
/ _ `/ _ \(_-</ __/ _ \/ _ \/ _  / / __/ // (_-<
\_,_/_.__/___/\__/\___/_//_/\_,_/_/\__/\_,_/___/
                        by d4no @danobt  
"""

# Enmarcar el mensaje de bienvenida
boxed_welcome = box_text(welcome_message)
print(boxed_welcome)

def vigenere_cipher_encrypt(text, keyword):
    text = text.upper()
    keyword = keyword.upper()
    keyword_repeated = (keyword * (len(text) // len(keyword) + 1))[:len(text)]
    encrypted_text = ''

    for t, k in zip(text, keyword_repeated):
        if t.isalpha():
            shift = ord(k) - ord('A')
            encrypted_char = chr((ord(t) - ord('A') + shift) % 26 + ord('A'))
            encrypted_text += encrypted_char
        else:
            encrypted_text += t

    return encrypted_text

def vigenere_cipher_decrypt(encrypted_text, keyword):
    keyword = keyword.upper()
    keyword_repeated = (keyword * (len(encrypted_text) // len(keyword) + 1))[:len(encrypted_text)]
    decrypted_text = ''

    for t, k in zip(encrypted_text, keyword_repeated):
        if t.isalpha():
            shift = ord(k) - ord('A')
            decrypted_char = chr((ord(t) - ord('A') - shift) % 26 + ord('A'))
            decrypted_text += decrypted_char
        else:
            decrypted_text += t

    return decrypted_text

def get_multiline_input(prompt):
    print(Fore.YELLOW + prompt + Style.RESET_ALL)
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return '\n'.join(lines)

def read_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    print(Fore.GREEN + "Elige una operación - '1' para Cifrado, '2' para Descifrado:" + Style.RESET_ALL)
    operation = input().strip()
    print(Fore.GREEN + "Ingresa '1' para escribir el texto, '2' para leer desde un archivo:" + Style.RESET_ALL)
    input_method = input().strip()

    if input_method == '1':
        text = get_multiline_input("Ingresa el texto (presiona Enter dos veces para terminar): ")
    elif input_method == '2':
        file_path = input(Fore.YELLOW + "Ingresa la ruta del archivo: " + Style.RESET_ALL)
        text = read_from_file(file_path)
    else:
        raise ValueError(Fore.RED + "Método de entrada inválido seleccionado." + Style.RESET_ALL)

    keyword = input(Fore.YELLOW + "Ingresa la palabra clave: " + Style.RESET_ALL)

    if operation == '1':
        result = vigenere_cipher_encrypt(text, keyword)
        print(Fore.MAGENTA + "\nMensaje Cifrado:\n" + result + Style.RESET_ALL)
    elif operation == '2':
        result = vigenere_cipher_decrypt(text, keyword)
        print(Fore.MAGENTA + "\nMensaje Descifrado:\n" + result + Style.RESET_ALL)
    else:
        raise ValueError(Fore.RED + "Operación inválida seleccionada." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
