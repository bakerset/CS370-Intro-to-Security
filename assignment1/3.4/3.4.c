#include <stdio.h>
#include <openssl/evp.h>
#include <string.h>
#include <sys/stat.h>
#include <ctype.h>

//check the length of the file
int check_file_length(const char* filename, size_t expected_length) {
    struct stat st;
    if (stat(filename, &st) != 0) {
        fprintf(stderr, "Error: Could not get file stats for %s\n", filename);
        return 0;
    }
    return st.st_size == expected_length;
}

//convert hex to bytes
void hex_to_bytes(const char* hex, unsigned char* bytes) {
    for (size_t i = 0; i < strlen(hex) / 2; i++) {
        sscanf(hex + 2 * i, "%2hhx", &bytes[i]);
    }
}

//check if decrypted text contains valid ASCII characters
int is_valid_ascii(unsigned char* text, int length) {
    for (int i = 0; i < length; i++) {
        if (!isprint(text[i]) && !isspace(text[i])) {
            return 0;
        }
    }
    return 1;
}

int main() {
    //check if the plaintext file length is exactly 21 bytes per requirement
    const char* plaintext_filename = "plain.txt";
    if (!check_file_length(plaintext_filename, 21)) {
        fprintf(stderr, "Error: Plaintext file is not 21 bytes long\n");
        return 1;
    }

    //define the ciphertext (given)
    const char* ciphertext_hex = "8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9"; 
    unsigned char ciphertext_bytes[EVP_MAX_BLOCK_LENGTH];
    hex_to_bytes(ciphertext_hex, ciphertext_bytes);
    
    //define your IV
    unsigned char iv[EVP_MAX_IV_LENGTH] = {0}; //all zeros similar to intructions

    //attempt to find the key from the word list
    FILE* wordlist = fopen("words.txt", "r");
    if (!wordlist) {
        fprintf(stderr, "Error: Could not open words.txt\n");
        return 1;
    }

    char key[17]; //16 + 1 for null terminator
    unsigned char decrypted_text[128];
    int decrypted_length;

    while (fgets(key, sizeof(key), wordlist)) {
        key[strcspn(key, "\n")] = 0; 

        //truncate the key if it’s longer than 16 characters
        if (strlen(key) > 16) {
            key[16] = '\0';
        }

        //pad key if necessary
        if (strlen(key) < 16) {
            memset(key + strlen(key), ' ', 16 - strlen(key)); //pad with spaces
            key[16] = '\0'; //null termination
        }

        //decrypt
        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
        if (!ctx) {
            fprintf(stderr, "Error: EVP_CIPHER_CTX_new failed\n");
            fclose(wordlist);
            return 1;
        }

        if (EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, (unsigned char*)key, iv) != 1) {
            fprintf(stderr, "Error: EVP_DecryptInit_ex failed\n");
            EVP_CIPHER_CTX_free(ctx);
            fclose(wordlist);
            return 1;
        }

        if (EVP_DecryptUpdate(ctx, decrypted_text, &decrypted_length, ciphertext_bytes, sizeof(ciphertext_bytes)) != 1) {
            fprintf(stderr, "Error: EVP_DecryptUpdate failed\n");
            EVP_CIPHER_CTX_free(ctx);
            fclose(wordlist);
            return 1;
        }

        //finalize decryption
        int final_length;
        if (EVP_DecryptFinal_ex(ctx, decrypted_text + decrypted_length, &final_length) == 1) {
            decrypted_length += final_length;
            decrypted_text[decrypted_length] = '\0'; //null terminate

            //only print the decrypted text if it's valid ASCII
            if (is_valid_ascii(decrypted_text, decrypted_length)) {
                printf("Key: '%s', Decrypted text: '%s'\n", key, decrypted_text);
                break; //exit the loop once the correct key is found
            }
        }

        EVP_CIPHER_CTX_free(ctx);
    }

    fclose(wordlist);
    return 0;
}
