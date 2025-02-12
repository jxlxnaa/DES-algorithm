import textwrap
import secrets

shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]

initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

exp_perm = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]

key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]

sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

pbox_perm = [16,  7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2,  8, 24, 14,
       32, 27,  3,  9,
       19, 13, 30,  6,
       22, 11,  4, 25]

def str2bin(plain_text):
    return ''.join(format(ord(i), '08b') for i in plain_text) 

def split_binary_text(bin_text):
    bytes = textwrap.wrap(bin_text, 64)
    bytes[-1] = bytes[-1] + (64-len(bytes[-1]))*"0"
    
    return bytes

def initial_permutation(byte_sequence):
    new_bytes = ["0" for _ in range(len(initial_perm))]

    for i in range(len(initial_perm)):
        new_bytes[i] = byte_sequence[initial_perm[i] - 1]

    return "".join(new_bytes)

def split_string(bytes):
    i = int(len(bytes)/2)

    return bytes[:i], bytes[i:]

def expansion_permutation(rpt):
    new_bytes = ["0" for _ in range(48)]

    for i in range(48):
        new_bytes[i] = rpt[exp_perm[i] - 1]

    return "".join(new_bytes)

def bytes_to_binary_string(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)

def generate_64_bit_key():
    random_bytes = secrets.token_bytes(8)  
    key_binary_string = bytes_to_binary_string(random_bytes)

    return key_binary_string

def reduce_key(key):
    new_key = ''.join([key[i:i+7] for i in range(0, len(key), 8)])

    return new_key

def key_shifting(key, n):    
    return key[n:] + key[:n]

def compression_permutation(byte_sequence):
    new_bytes = ["0" for _ in range(len(key_comp))]

    for i in range(len(key_comp)):
        new_bytes[i] = byte_sequence[key_comp[i] - 1]

    return "".join(new_bytes)

def key_transformation(key1, key2, n):
    key1 = key_shifting(key1, n)
    key2 = key_shifting(key2, n)
    key = key1 + key2

    return key

def xor_binary_strings(str1, str2):
    return ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(str1, str2))

def bin2int(binary_string):
    decimal_integer = int(binary_string, 2)

    return decimal_integer
    
def s_box(xored_rpt):
    s_box_output = []
    j = 0

    for i in range(0, 48, 6):
        s_box_input = xored_rpt[i:i+6]
        idx1 = s_box_input[0] + s_box_input[5]
        idx1 = bin2int(idx1)
        idx2 = s_box_input[1] + s_box_input[2] + s_box_input[3] + s_box_input[4]
        idx2 = bin2int(idx2)
        s_box_output.append(sbox[j][idx1][idx2])
        j += 1

    binary_strings = [format(num, '04b') for num in s_box_output]
    result = ''.join(binary_strings)

    return result

def pbox_permutation(byte_sequence):
    new_bytes = ["0" for _ in range(len(pbox_perm))]

    for i in range(len(pbox_perm)):
        new_bytes[i] = byte_sequence[pbox_perm[i] - 1]

    return "".join(new_bytes)

def final_permutation(byte_sequence):
    new_bytes = ["0" for _ in range(len(final_perm))]

    for i in range(len(final_perm)):
        new_bytes[i] = byte_sequence[final_perm[i] - 1]

    return "".join(new_bytes)

def bin2str(binary_text):
    chunks = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    result_str = ''.join(chr(int(chunk, 2)) for chunk in chunks)

    return result_str

def swap_halves(bits_list):
    swapped_list = []

    for bits_string in bits_list:
        first_half = bits_string[:32]
        second_half = bits_string[32:]
        swapped_string = second_half + first_half
        swapped_list.append(swapped_string)

    return swapped_list

def encryption(byte_sequences, key):
    key = compression_permutation(key) 
    splited_bytes = list(map(split_string, byte_sequences)) 
    lpt, rpt = [el[0] for el in splited_bytes], [el[1] for el in splited_bytes] 
    rpt_extended = list(map(expansion_permutation, rpt))
    l_output = []
    
    for j in range(len(rpt_extended)):
        xored_rpt = xor_binary_strings(rpt_extended[j], key)
        s_box_output = s_box(xored_rpt)
        p_box_output = pbox_permutation(s_box_output)
        xored_pbox = xor_binary_strings(lpt[j], p_box_output)
        l_output.append(xored_pbox)

    result_list = [a + b for a, b in zip(l_output, rpt)]

    return result_list

def main():
    plain_text = "Cryptography"
    byte_sequences = split_binary_text(str2bin(plain_text))
    byte_permutation_encryption = list(map(initial_permutation, byte_sequences))

    # KEY
    key = generate_64_bit_key() 
    new_key = reduce_key(key)
    new_key1, new_key2 = split_string(new_key)
    key_list = []

    # ENCRYPTION
    for i in range(16):
        key = key_transformation(new_key1, new_key2, shift_table[i])
        new_key1, new_key2 = split_string(key)
        key_list.append(key)
        encrypted_message = encryption(byte_permutation_encryption, key)
        byte_permutation_encryption = swap_halves(encrypted_message)

    encrypted_message = swap_halves(byte_permutation_encryption)
    encrypted_message = list(map(final_permutation, encrypted_message)) 

    # DECRYPTION
    byte_permutation_decryption = list(map(initial_permutation, encrypted_message)) 

    for key in reversed(key_list):
        decrypted_message = encryption(byte_permutation_decryption, key)
        byte_permutation_decryption = swap_halves(decrypted_message)

    decrypted_message = swap_halves(byte_permutation_decryption)
    decrypted_message = list(map(final_permutation, decrypted_message))
    

    # PRINT
    print('Plain text: ', plain_text)
    print('Message binary: ', str2bin(plain_text))

    encrypted_message = "".join(encrypted_message)
    print('Encrypted message: ', encrypted_message)
    
    decrypted_message = "".join(decrypted_message)
    print('Decrypted message: ', decrypted_message)

    decrypted_message = bin2str(decrypted_message)
    print('Plain text decrypted: ', decrypted_message)

main()
