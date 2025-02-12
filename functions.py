import textwrap
import secrets
from constants import initial_perm, final_perm, exp_perm, key_comp, sbox, pbox_perm


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