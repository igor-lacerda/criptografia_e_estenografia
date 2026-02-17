import gmpy2
import random

def generate_large_prime(
    size: int = 1024
) -> gmpy2.mpz:
    """
    Gera um primo grande.
    """
    num = random.randrange(2 ** (size - 1), 2 ** size)
    return gmpy2.next_prime(num)

def generate_key(
    size: int = 1024
) -> tuple[int, int]:
    """
    Gera as chaves pública e privada.
    """
    p = 0
    q = 0
    while p == q:
        p = generate_large_prime(size)
        q = generate_large_prime(size)
    
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    while True:
        # Chave pública, utilizada para encriptar a mensagem
        e = generate_large_prime()
        # Verifica se são primos entre si
        if gmpy2.gcd(e, phi_n) == 1: break

    # Mod inverse
    d = gmpy2.invert(e, phi_n)

    return ((int(n), int(e)), (int(n), int(d)))

def make_key_files(
    name: str, 
    size: int = 1024
) -> None:
    """
    Cria os arquivos com as chaves.
    """
    try:
        public_key, private_key = generate_key(size)
        with open(f"{name}_public_key.txt", "w") as file:
            file.write(f"{size},{public_key[0]},{public_key[1]}")
        
        with open(f"{name}_private_key.txt", "w") as file:
            file.write(f"{size},{private_key[0]},{private_key[1]}")
    except PermissionError:
        print("Sem permissão para abrir o arquivo")

def read_key_file(
    key_filename : str
) -> tuple[int, int, int]:
    """
    Processa as chaves a partir de um arquivo.
    """
    with open(key_filename) as file:
        content = file.read()
    key_size, n, e_or_d = content.split(",")

    return (int(key_size), int(n), int(e_or_d))

def get_blocks_from_text(
    message: str, 
    block_size: int
) -> list[int]:
    """
    Converte string para blocos de inteiros (Bytes/UTF-8).
    """
    message_bytes = message.encode("utf-8")
    block_integers = []

    for i in range(0, len(message_bytes), block_size):
        chunk = message_bytes[i : i + block_size]
        block_int = int.from_bytes(chunk, byteorder="big")
        block_integers.append(block_int)

    return block_integers

def get_text_from_blocks(
    block_integers: list[int]
) -> str:
    """
    Converte blocos de inteiros de volta para o formato de string.
    """
    message_bytes_list = []

    for block_int in block_integers:
        # Descobre quantos bytes são necessários para representar este número.
        # A fórmula é: ceil(bit_length / 8). No entanto, (bit_length + 7) // 8 é a forma inteira de fazer arredondamento para cima.
        num_bytes = (block_int.bit_length() + 7) // 8
        
        # Se o bloco for 0, bit_length é 0, mas precisa-se de 1 byte.
        if num_bytes == 0:
            num_bytes = 1

        try:
            # Converte o inteiro de volta para bytes
            chunk = block_int.to_bytes(num_bytes, byteorder="big")
            message_bytes_list.append(chunk)
        except OverflowError:
            print(f"Erro ao converter bloco: {block_int}")

    full_message_bytes = b"".join(message_bytes_list)
    return full_message_bytes.decode("utf-8", errors="replace")

def encrypt_to_blocks(
    message: str, 
    key : int, 
    block_size: int = None
) -> list[int]:
    """
    Padrão matemático da encriptação RSA.
    """
    encrypted_blocks = list()
    n, e = key
    blocks_from_text = get_blocks_from_text(message, block_size)
    
    for block in blocks_from_text:
        encrypted_blocks.append(pow(block, e, n))
    
    return encrypted_blocks

def decrypt_from_blocks(
    encrypted_blocks: list[int], 
    key: tuple[int, int]
) -> str:
    """
    Padrão matemático de decriptação.
    """
    decrypted_blocks = list()
    n, d = key
    
    for block in encrypted_blocks:
        decrypted_blocks.append(pow(block, d, n))

    return get_text_from_blocks(decrypted_blocks)

def encrypt_message(
    message: str, 
    key_filename: str, 
    block_size: int = None
) -> str:
    """
    Core Function: Realiza todo o processo de encriptação e formatação.
    """
    key_size, n, e = read_key_file(key_filename)

    # Lógica de cálculo do tamanho do bloco de inteiros
    if block_size is None:
        # Tamanho da chave em bytes - 1, posto que o tamanho de um bloco de inteiros m deve menor que n.
        block_size = (key_size // 8) - 1
    
    # Verificação de segurança se block_size for fornecido pelo usuário
    if block_size >= (key_size // 8):
        raise ValueError(f"Aviso: Block size {block_size} está demasiadamente próximo ou acima do tamanho da chave.")

    # Encriptação
    encrypted_blocks = encrypt_to_blocks(message, (n, e), block_size)
    
    # Formatação final (blocksize_conteudo)
    encrypted_content = ",".join(map(str, encrypted_blocks))
    return f"{block_size}_{encrypted_content}"

def decrypt_message(
    encrypted_string: str, 
    key_filename: str
) -> str:
    """
    Core Function: Realiza todo o processo de parsing e decriptação.
    """
    key_size, n, d = read_key_file(key_filename)

    # Parsing da string
    try:
        block_size_str, encrypted_message_str = encrypted_string.split("_", 1)
        block_size = int(block_size_str)
    except ValueError:
        raise ValueError("A string fornecida não está no formato correto 'tamanhoBloco_dados'.")

    # Verifica se o bloco (em bytes) cabe dentro da chave (também em bytes).
    if block_size > (key_size // 8):
        raise ValueError("ERRO: O tamanho do bloco é maior que a capacidade da chave.")

    # Converte a string de dados de volta para lista de inteiros
    encrypted_blocks = [int(block) for block in encrypted_message_str.split(",")]
    
    return decrypt_from_blocks(encrypted_blocks, (n, d))

def encrypt_and_write_to_file(
    message_filename: str, 
    key_filename: str, 
    message: str, 
    block_size = None
) -> None:
    """
    Wrapper: Usa a lógica de encrypt_message e salva em disco.
    """
    encrypted_content = encrypt_message(message, key_filename, block_size)
    
    with open(message_filename, "w") as file:
        file.write(encrypted_content)

def read_from_file_and_decrypt(
    message_filename: str, 
    key_filename: str
) -> str:
    """
    Wrapper: Lê do disco e usa a lógica de decrypt_message.
    """
    with open(message_filename, "r") as file:
        content = file.read()
    
    return decrypt_message(content, key_filename)

def main():
    # Exemplo
    name = "Maria"
    message = "Tempus fugit"
    filename = "encrypted_file.txt"

    make_key_files(name)

    private_key_filename = f"{name}_private_key.txt"
    public_key_filename = f"{name}_public_key.txt"

    # Encriptação
    encrypted_message = encrypt_message(message, public_key_filename)
    # encrypt_and_write_to_file(filename, public_key_filename, message)
    print(encrypted_message)

    # Decriptação
    decrypted_message = decrypt_message(encrypted_message, private_key_filename)
    # decrypted_message = read_from_file_and_decrypt(filename, private_key_filename)
    print(decrypted_message)

if __name__ == "__main__":
    main()
