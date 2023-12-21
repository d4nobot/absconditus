import subprocess
import sys
from colorama import Fore, Style
from cryptography.fernet import Fernet

# Función para instalar e importar un paquete de Python
def install_and_import(paquete):
    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
    __import__(paquete)

# Lista de paquetes requeridos
paquetes_requeridos = ["colorama", "cryptography"]

# Instalar paquetes requeridos
for paquete in paquetes_requeridos:
    try:
        __import__(paquete)
    except ImportError:
        print(f"Instalando {paquete}...")
        install_and_import(paquete)

try:
    import colorama
    from colorama import Fore, Style
except ImportError:
    print("Colorama no está instalado y no se puede instalar automáticamente.")
    sys.exit(1)

colorama.init(autoreset=True)

def box_text(texto, padding=1):
    líneas = texto.split('\n')
    max_ancho = max(len(línea) for línea in líneas)
    ancho_caja = max_ancho + 2 * padding

    arriba_abajo = '+' + '-' * ancho_caja + '+'
    líneas_rellenas = [f"|{' ' * padding}{línea}{' ' * (ancho_caja - len(línea))}|" for línea in líneas]

    texto_encajado = [arriba_abajo] + líneas_rellenas + [arriba_abajo]
    return '\n'.join(texto_encajado)

mensaje_bienvenida = r"""
       __                        ___ __         
 ___ _/ /  ___ _______  ___  ___/ (_) /___ _____
/ _ `/ _ \(_-</ __/ _ \/ _ \/ _  / / __/ // (_-<
\_,_/_.__/___/\__/\___/_//_/\_,_/_/\__/\_,_/___/
                        por d4no @danobt  
"""

caja_mensaje_bienvenida = box_text(mensaje_bienvenida)
print(caja_mensaje_bienvenida)

# Implementa tus funciones de cifrado Vigenère aquí
def vigenere_cipher_encrypt(texto, palabra_clave):
    resultado = []
    longitud_palabra_clave = len(palabra_clave)
    for i, carácter in enumerate(texto):
        if carácter.isalpha():
            desplazamiento = ord(palabra_clave[i % longitud_palabra_clave].lower()) - ord('a')
            if carácter.islower():
                resultado.append(chr(((ord(carácter) - ord('a') + desplazamiento) % 26) + ord('a')))
            else:
                resultado.append(chr(((ord(carácter) - ord('A') + desplazamiento) % 26) + ord('A')))
        else:
            resultado.append(carácter)
    return ''.join(resultado)

def vigenere_cipher_decrypt(texto, palabra_clave):
    resultado = []
    longitud_palabra_clave = len(palabra_clave)
    for i, carácter in enumerate(texto):
        if carácter.isalpha():
            desplazamiento = ord(palabra_clave[i % longitud_palabra_clave].lower()) - ord('a')
            if carácter.islower():
                resultado.append(chr(((ord(carácter) - ord('a') - desplazamiento) % 26) + ord('a')))
            else:
                resultado.append(chr(((ord(carácter) - ord('A') - desplazamiento) % 26) + ord('A')))
        else:
            resultado.append(carácter)
    return ''.join(resultado)

def caesar_cipher(texto, desplazamiento, cifrar=True):
    resultado = []
    for carácter in texto:
        if carácter.isalpha():
            if carácter.islower():
                resultado.append(chr(((ord(carácter) - ord('a') + desplazamiento) % 26) + ord('a')) if cifrar else chr(((ord(carácter) - ord('a') - desplazamiento) % 26) + ord('a')))
            else:
                resultado.append(chr(((ord(carácter) - ord('A') + desplazamiento) % 26) + ord('A')) if cifrar else chr(((ord(carácter) - ord('A') - desplazamiento) % 26) + ord('A')))
        else:
            resultado.append(carácter)
    return ''.join(resultado)

def reverse_cipher(texto, cifrar=True):
    return texto[::-1] if cifrar else texto[::-1]


# ... (The rest of your functions)

if __name__ == "__main__":
    # Generate a random Fernet key
    key = Fernet.generate_key()

    # Print the key (you can save it for later use)
    print(key)

    def guardar_a_archivo(contenido, nombre_archivo):
        with open(nombre_archivo + ".txt", 'w') as archivo:
            archivo.write(contenido)
        print(Fore.GREEN + "Salida guardada en " + nombre_archivo + ".txt" + Style.RESET_ALL)

    def encrypt_decrypt(texto, método, palabra_clave=None, cifrar=True):
        if método == 'vigenere':
            return vigenere_cipher_encrypt(texto, palabra_clave) if cifrar else vigenere_cipher_decrypt(texto, palabra_clave)
        elif método == 'caesar':
            desplazamiento = int(input(Fore.YELLOW + "Ingrese el valor de desplazamiento: " + Style.RESET_ALL))
            return caesar_cipher(texto, desplazamiento, cifrar)
        elif método == 'reverse':
            return reverse_cipher(texto, cifrar)
        else:
            raise ValueError(Fore.RED + "Método desconocido: " + método + Style.RESET_ALL)

    def obtener_entrada_multilínea(prompt):
        print(Fore.YELLOW + prompt + Style.RESET_ALL)
        líneas = []
        while True:
            línea = input()
            if línea:
                líneas.append(línea)
            else:
                break
        return '\n'.join(líneas)

    def leer_desde_archivo(ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            return archivo.read()

    # Función para cifrar un archivo
    def cifrar_archivo(ruta_archivo, ruta_salida, contraseña):
        try:
            # Leer el contenido del archivo
            with open(ruta_archivo, 'rb') as archivo:
                datos_archivo = archivo.read()

            # Cifrar el contenido del archivo
            suite_cifrado = Fernet(contraseña)
            datos_cifrados = suite_cifrado.encrypt(datos_archivo)

            # Escribir el contenido cifrado en un nuevo archivo
            with open(ruta_salida, 'wb') as archivo_cifrado:
                archivo_cifrado.write(datos_cifrados)

            print(Fore.GREEN + "Archivo cifrado con éxito: " + ruta_salida + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Error al cifrar el archivo: " + str(e) + Style.RESET_ALL)

    def procesar_archivos():
        print(Fore.GREEN + "Ingrese la operación - 1 para Cifrar, 2 para Descifrar:" + Style.RESET_ALL)
        operación = int(input().strip())  # Convertir a entero

        contraseña = input(Fore.YELLOW + "Ingrese la contraseña para cifrar/descifrar el archivo: " + Style.RESET_ALL)

        if operación == 1:
            # Cifrar archivo
            ruta_archivo = input(Fore.YELLOW + "Ingrese la ruta del archivo para cifrar: " + Style.RESET_ALL)
            ruta_salida = input(Fore.YELLOW + "Ingrese la ruta para guardar el archivo cifrado: " + Style.RESET_ALL)
            cifrar_archivo(ruta_archivo, ruta_salida, contraseña)
        elif operación == 2:
            # Descifrar archivo
            ruta_archivo = input(Fore.YELLOW + "Ingrese la ruta del archivo para descifrar: " + Style.RESET_ALL)
            ruta_salida = input(Fore.YELLOW + "Ingrese la ruta para guardar el archivo descifrado: " + Style.RESET_ALL)
            descifrar_archivo(ruta_archivo, ruta_salida, contraseña)
        else:
            print(Fore.RED + "Operación no válida seleccionada." + Style.RESET_ALL)

    def main():
        print(Fore.GREEN + "Elija una operación - 1 para Cifrar, 2 para Descifrar, 3 para Procesar Archivos:" + Style.RESET_ALL)
        operación = int(input().strip())  # Convertir a entero

        if operación == 1 or operación == 2:
            # Cifrar o descifrar texto
            método_input = input(Fore.GREEN + "Ingrese el método de cifrado: vigenere, caesar, reverse" + Style.RESET_ALL)
            if método_input not in ['vigenere', 'caesar', 'reverse']:
                raise ValueError(Fore.RED + "Método desconocido: " + método_input + Style.RESET_ALL)
            método = método_input

            texto = ''
            if operación in [1, 2]:
                print(Fore.GREEN + "Ingrese '1' para ingresar texto, '2' para leer desde un archivo:" + Style.RESET_ALL)
                método_entrada = input().strip()

                if método_entrada == '1':
                    texto = obtener_entrada_multilínea("Ingrese el texto (presione Enter dos veces para finalizar): ")
                elif método_entrada == '2':
                    ruta_archivo = input(Fore.YELLOW + "Ingrese la ruta del archivo: " + Style.RESET_ALL)
                    texto = leer_desde_archivo(ruta_archivo)
                else:
                    raise ValueError(Fore.RED + "Método de entrada no válido seleccionado." + Style.RESET_ALL)

            palabra_clave = ''
            if método == 'vigenere':
                palabra_clave = input(Fore.YELLOW + "Ingrese la palabra clave: " + Style.RESET_ALL)

            resultado = ''
            if operación == 1:
                resultado = encrypt_decrypt(texto, método, palabra_clave, True)
            elif operación == 2:
                resultado = encrypt_decrypt(texto, método, palabra_clave, False)
            else:
                raise ValueError(Fore.RED + "Operación no válida seleccionada." + Style.RESET_ALL)

            print(Fore.MAGENTA + "\nResultado:\n" + resultado + Style.RESET_ALL)

            if input(Fore.CYAN + "¿Desea guardar el resultado en un archivo? (s/n): " + Style.RESET_ALL).lower() == 's':
                nombre_archivo = input(Fore.YELLOW + "Ingrese el nombre de archivo para guardar la salida: " + Style.RESET_ALL)
                guardar_a_archivo(resultado, nombre_archivo)
        elif operación == 3:
            # Procesar archivos
            procesar_archivos()
        else:
            print(Fore.RED + "Operación no válida seleccionada." + Style.RESET_ALL)

    if __name__ == "__main__":
        main()
# ... (Previous code from Part 1)

# ... (Continuation of your functions from Part 1)

def procesar_archivos():
    print(Fore.GREEN + "Ingrese la operación - 1 para Cifrar, 2 para Descifrar:" + Style.RESET_ALL)
    operación = int(input().strip())  # Convertir a entero

    contraseña = input(Fore.YELLOW + "Ingrese la contraseña para cifrar/descifrar el archivo: " + Style.RESET_ALL)

    if operación == 1:
        # Cifrar archivo
        ruta_archivo = input(Fore.YELLOW + "Ingrese la ruta del archivo para cifrar: " + Style.RESET_ALL)
        ruta_salida = input(Fore.YELLOW + "Ingrese la ruta para guardar el archivo cifrado: " + Style.RESET_ALL)
        cifrar_archivo(ruta_archivo, ruta_salida, contraseña)
    elif operación == 2:
        # Descifrar archivo
        ruta_archivo = input(Fore.YELLOW + "Ingrese la ruta del archivo para descifrar: " + Style.RESET_ALL)
        ruta_salida = input(Fore.YELLOW + "Ingrese la ruta para guardar el archivo descifrado: " + Style.RESET_ALL)
        descifrar_archivo(ruta_archivo, ruta_salida, contraseña)
    else:
        print(Fore.RED + "Operación no válida seleccionada." + Style.RESET_ALL)

def main():
    print(Fore.GREEN + "Elija una operación - 1 para Cifrar, 2 para Descifrar, 3 para Procesar Archivos:" + Style.RESET_ALL)
    operación = int(input().strip())  # Convertir a entero

    if operación == 1 or operación == 2:
        # Cifrar o descifrar texto
        método_input = input(Fore.GREEN + "Ingrese el método de cifrado: vigenere, caesar, reverse" + Style.RESET_ALL)
        if método_input not in ['vigenere', 'caesar', 'reverse']:
            raise ValueError(Fore.RED + "Método desconocido: " + método_input + Style.RESET_ALL)
        método = método_input

        texto = ''
        if operación in [1, 2]:
            print(Fore.GREEN + "Ingrese '1' para ingresar texto, '2' para leer desde un archivo:" + Style.RESET_ALL)
            método_entrada = input().strip()

            if método_entrada == '1':
                texto = obtener_entrada_multilínea("Ingrese el texto (presione Enter dos veces para finalizar): ")
            elif método_entrada == '2':
                ruta_archivo = input(Fore.YELLOW + "Ingrese la ruta del archivo: " + Style.RESET_ALL)
                texto = leer_desde_archivo(ruta_archivo)
            else:
                raise ValueError(Fore.RED + "Método de entrada no válido seleccionado." + Style.RESET_ALL)

        palabra_clave = ''
        if método == 'vigenere':
            palabra_clave = input(Fore.YELLOW + "Ingrese la palabra clave: " + Style.RESET_ALL)

        resultado = ''
        if operación == 1:
            resultado = encrypt_decrypt(texto, método, palabra_clave, True)
        elif operación == 2:
            resultado = encrypt_decrypt(texto, método, palabra_clave, False)
        else:
            raise ValueError(Fore.RED + "Operación no válida seleccionada." + Style.RESET_ALL)

        print(Fore.MAGENTA + "\nResultado:\n" + resultado + Style.RESET_ALL)

        if input(Fore.CYAN + "¿Desea guardar el resultado en un archivo? (s/n): " + Style.RESET_ALL).lower() == 's':
            nombre_archivo = input(Fore.YELLOW + "Ingrese el nombre de archivo para guardar la salida: " + Style.RESET_ALL)
            guardar_a_archivo(resultado, nombre_archivo)
    elif operación == 3:
        # Procesar archivos
        procesar_archivos()
    else:
        print(Fore.RED + "Operación no válida seleccionada." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
# ... (Previous code from Part 2)

# ... (Continuation of your functions from Part 2)

def descifrar_archivo(ruta_archivo, ruta_salida, contraseña):
    try:
        # Leer el contenido cifrado del archivo
        with open(ruta_archivo, 'rb') as archivo:
            datos_cifrados = archivo.read()

        # Descifrar el contenido del archivo
        suite_cifrado = Fernet(contraseña)
        datos_descifrados = suite_cifrado.decrypt(datos_cifrados)

        # Escribir el contenido descifrado en un nuevo archiavo
        with open(ruta_salida, 'wb') as archivo_descifrado:
            archivo_descifrado.write(datos_descifrados)

        print(Fore.GREEN + "Archivo descifrado con éxito: " + ruta_salida + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "Error al descifrar el archivo: " + str(e) + Style.RESET_ALL)

# ... (Continuation of your functions)

if __name__ == "__main__":
    main() 