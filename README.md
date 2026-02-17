# Implementações de Criptografia em Python

Este repositório é uma espécie de "laboratório" pessoal para estudos de criptografia, algoritmos, estenografia e manipulação de dados em estruturas de baixo nível. Aqui há algumas implementações de cifras históricas e modernas adaptadas para para fins de exercícios computacionais, explorando aspectos matemáticos a respeito de números primos até a codificação de imagens.

## Motivações

Eu comecei a me interessar por criptografia por curiosidade em Matemática e História e, sobretudo, ao conhecer o livro *Cracking Codes With Python* de Al Sweigart. Contudo, conforme eu progredia nos tópicos abordados no livro, tive a necessidade, bem como o interesse, de me aprofundar nos assuntos e torná-lo como alicerce para parte dos meus estudos em programação. O repositório apresenta um conjunto de cifras para diferentes estruturas de dados, como strings e imagens, e tem por finalidade ser um "laboratório" de estudos de codificação e manipulação de dados.

## Conteúdo do Repositório

O projeto está dividido em módulos focados em diferentes tipos de cifragem:

### RSA (Cifra de Chave Pública/Privada)

Implementação "from scratch" do algoritmo RSA, com foco na compreensão da aritmética modular e geração de números primos grandes.

* **Bibliotecas:** Utiliza `gmpy2` para precisão aritmética e performance com números inteiros grandes.
* **Funcionalidades:**
* Geração de chaves (Pública e Privada) com primos de `n` bits.
* Sistema de blocos: Converte strings (UTF-8) em blocos numéricos para permitir a encriptação de mensagens maiores que a chave.
* Persistência: Salva e lê chaves e mensagens cifradas em arquivos `.txt`.

### Cifra de Vigenère para Imagens

Arquivo: `vigenere_cipher_image.py`

Uma adaptação da cifra de Vigenère aplicada à manipulação de pixels em imagens com `numpy` e `OpenCV`.

A criptografia de Vigenère é tipicamente implementada com uso da cifra de César para encriptação. No entanto, como esta cifra é essencialmente uma transformação linear de translação, a aplicação à uma imagem resultaria em uma mera troca de cores, razoavelmente uniforme a depender da chave de encriptação. Com uma cifra multiplicativa, ao invés de aditiva como é a de César, é possível codificar a imagem com uma espécie de ruído, visualmente protegendo a informação que se quer transmitir. Por essa razão, a função faz uso de um Vigenère combinado com "Affine Cipher" e não puramente aditivo, como a tradicional.


## Instalação e Dependências

Os scripts deste repositório usam as seguintes bibliotecas externas:

```bash
pip install gmpy2 numpy opencv-python

```

*Nota: A instalação do `gmpy2` pode exigir bibliotecas de sistema adicionais (como MPC, MPFR e GMP) dependendo do seu sistema operacional.*

## Ovservação

Este repositório tem fins estritamente **educacionais**. As implementações aqui presentes servem para entender a lógica matemática por trás dos algoritmos.

* Não faça uso deste código para proteger dados sensíveis.
* Para segurança real, sugere-se bibliotecas como `cryptography` ou `PyCryptodome`.

