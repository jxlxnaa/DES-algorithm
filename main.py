from functions import split_binary_text, str2bin, initial_permutation, generate_64_bit_key, reduce_key, split_string, key_transformation, encryption, swap_halves, final_permutation, bin2str
from constants import shift_table

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
