import numpy as np
import cv2
from pathlib import Path

def vigenere_cipher_image(
    image: np.ndarray,
    key: str,
    mode: str = "encrypt"
) -> np.ndarray: 
    """
    Aplica a cifra de Vigenère multiplicativa ("Affine Cipher" ao invés de Cifra de César) em uma imagem.
    Retorna um array com a imagem processada.

    :param image: Array de numpy da imagem de entrada (geralmente carregada com o opencv).
    :param key: String utilizada como chave de encriptação, gerará os fatores multiplicativos.
    :param mode: Define o modo de operação da função de encriptação ou decriptação, respectivamente 'encrypt' ou 'decrypt'.
    """
    if mode not in ["encrypt", "decrypt"]:
        raise ValueError("Valor de 'mode' deve ser 'encrypt' ou 'decrypt'.")

    flat_img = image.flatten().astype(np.int32)
    flat_size = flat_img.size

    # Alocando memória previamente
    cipher_img = np.zeros_like(flat_img)

    key_values = [ord(char) | 1 for char in key]
    # Coeficiente linear
    key_offset = sum(key_values) % 256

    if mode == "encrypt":
        # É necessário reescrever a senha em termos de valores coprimos de 256
        key_arr = np.resize(key_values, flat_size)

        # Na encriptação, primeiro soma-se o coeficiente linear e depois multiplica-se
        flat_img = flat_img + key_offset
        flat_img = flat_img * key_arr

        cipher_img = flat_img
        cipher_img = (flat_img % 256).astype(np.uint8)
    else: # "decrypt"
        # Calcula-se o inverso modular
        key_values = [pow(k, -1, 256) for k in key_values]
        key_arr = np.resize(key_values, flat_size)

        flat_img = flat_img * key_arr
        flat_img = flat_img - key_offset

    cipher_img = (flat_img % 256).astype(np.uint8)    
    return cipher_img.reshape(image.shape)

def cipher_images_from_directory(
    source_dir: str,
    key: str,
    mode: str = "encrypt",
    output_dir: str = None
) -> None:

    """
    Criptografa todas as imagens de um diretório.
    """
    input_path = Path(source_dir)

    # Configura o diretório de saída das imagens
    if output_dir is None:
        suffix = "_encrypted" if mode == "encrypt" else "_restored"
        save_path = input_path / ("images" + suffix)
    else:
        save_path = Path(output_dir)
    
    save_path.mkdir(parents=True, exist_ok=True)

    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

    for file in input_path.iterdir():
        if file.suffix.lower() in valid_extensions:
            image = cv2.imread(str(file))

            if image is None:
                print(f"Arquivo corrompido ou inválido: {file.name}")
                continue
            
            try:
                processed_image = vigenere_cipher_image(image, key, mode)

                output_file = save_path / (file.stem + ".png")
                cv2.imwrite(str(output_file), processed_image)
            except Exception as e:
                print(f"Erro ao processar {file.name}: {e}")

def main():
    # Exemplo
    image = r"C:\Users\Administrator\Desktop\exemplo.jpg"
    img = cv2.imread(image)

    key = "Mona Lisa"

    # Encriptação
    cipher_img = vigenere_cipher_image(img, key, mode = "encrypt")
    cv2.imwrite(r"C:\Users\Administrator\Desktop\exemplo_codificado.png", cipher_img)

    # Decriptação
    reconstruted_img = vigenere_cipher_image(cipher_img, key, mode = "decrypt")
    cv2.imwrite(r"C:\Users\Administrator\Desktop\exemplo_recuperado.png", reconstruted_img)

    # cipher_images_from_directory(r"C:\Users\Administrator\Desktop\exemplo", key, "encrypt")

if __name__ == "__main__":
    main()
