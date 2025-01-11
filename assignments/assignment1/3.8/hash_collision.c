#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <openssl/evp.h>
#include <openssl/sha.h>

#define HASH_LENGTH 3 //or 24 bits
#define MAX_INPUT_LENGTH 3 //limits input length to 3
#define CHARSET_SIZE 26 //charset - alphabet size
#define TRIALS 100 //num exp

//function to compute the hash and return the first 3 bytes
void compute_hash(const char *input, unsigned char *output) {
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    const EVP_MD *md = EVP_sha256();
    unsigned int output_length;

    EVP_DigestInit_ex(ctx, md, NULL);
    EVP_DigestUpdate(ctx, input, strlen(input));
    EVP_DigestFinal_ex(ctx, output, &output_length); //full hash output

    memcpy(output, output, HASH_LENGTH); //store result in output

    EVP_MD_CTX_free(ctx); //free memory
}

//function to test weak collision resistance and return the number of trials
int test_weak_collision(int *found_collision) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    char input[MAX_INPUT_LENGTH + 1];
    unsigned char (*seen_hashes)[HASH_LENGTH] = malloc((1 << (HASH_LENGTH * 8)) * sizeof(*seen_hashes));
    if (seen_hashes == NULL) {
        perror("Failed to allocate memory for seen_hashes");
        exit(EXIT_FAILURE);
    }

    int seen_count = 0;
    int trials = 0;

    //randomized (brute force - char) inputs
    while (trials < (1 << (MAX_INPUT_LENGTH * 5))) {
        //generated a random input string
        for (int j = 0; j < MAX_INPUT_LENGTH; j++) {
            input[j] = 'a' + (rand() % CHARSET_SIZE); //random character from 'a' to 'z'
        }
        input[MAX_INPUT_LENGTH] = '\0'; //null term the string

        compute_hash(input, hash);
        trials++;

        //check against all previous inputs for a weak collision
        for (int k = 0; k < seen_count; k++) {
            //compare hashes
            if (memcmp(hash, seen_hashes[k], HASH_LENGTH) == 0) {
                free(seen_hashes);
                *found_collision = 1; //indicate a collision was found
                return trials;
            }
        }

        if (seen_count < (1 << (HASH_LENGTH * 8))) {
            memcpy(seen_hashes[seen_count++], hash, HASH_LENGTH);
        }

        if (trials % 100000 == 0) {
            printf("Weak collision trials so far: %d\n", trials);
        }
    }

    free(seen_hashes);
    return trials; //return max trials if no collision found
}

//function to test strong collision resistance and return the number of trials
int test_strong_collision(int *found_collision) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    unsigned char (*seen_hashes)[HASH_LENGTH] = malloc((1 << (HASH_LENGTH * 8)) * sizeof(*seen_hashes));
    if (seen_hashes == NULL) {
        perror("Failed to allocate memory for seen_hashes");
        exit(EXIT_FAILURE);
    }

    char input[MAX_INPUT_LENGTH + 1];
    int seen_count = 0;
    int trials = 0;

    //same as weak collision but for strong collision
    while (trials < (1 << (MAX_INPUT_LENGTH * 5))) {
        for (int j = 0; j < MAX_INPUT_LENGTH; j++) {
            input[j] = 'a' + (rand() % CHARSET_SIZE);
        }
        input[MAX_INPUT_LENGTH] = '\0';

        compute_hash(input, hash);
        trials++;

        //check against all previous inputs for a strong collision
        for (int j = 0; j < seen_count; j++) {
            //compare hashes
            if (memcmp(hash, seen_hashes[j], HASH_LENGTH) == 0) {
                free(seen_hashes);
                *found_collision = 1;
                return trials;
            }
        }

        if (seen_count < (1 << (HASH_LENGTH * 8))) {
            memcpy(seen_hashes[seen_count++], hash, HASH_LENGTH);
        }

        if (trials % 100000 == 0) {
            printf("Strong collision trials so far: %d\n", trials);
        }
    }

    free(seen_hashes);
    return trials;
}

int main() {
    srand(time(NULL)); //seeding the random number generator

    //initializations
    int found_weak_collision = 0;
    int found_strong_collision = 0;
    double weak_average = 0.0;
    double strong_average = 0.0;

    //run trials for weak collisions
    for (int i = 0; i < TRIALS; i++) {
        int trials = test_weak_collision(&found_weak_collision);
        if (found_weak_collision) {
            weak_average += trials;
            printf("Found weak collision after %d trials!\n", trials);
        }
        found_weak_collision = 0; //reset for next trial - helps data errors
    }
    weak_average /= TRIALS; //avg

    //run trials for strong collisions
    for (int i = 0; i < TRIALS; i++) {
        int trials = test_strong_collision(&found_strong_collision);
        strong_average += trials;
        if (found_strong_collision) {
            printf("Found strong collision after %d trials!\n", trials);
        }
        found_strong_collision = 0;
    }
    strong_average /= TRIALS;

    //results
    printf("Average trials to break weak collision resistance: %.2f\n", weak_average);
    printf("Average trials to break strong collision resistance: %.2f\n", strong_average);

    //observations
    if (weak_average == strong_average) {
        printf("Weak and strong collision resistance are the same.\n");
    } else if (weak_average < strong_average) {
        printf("Weak collision resistance is easier to break than strong collision resistance.\n");
    } else {
        printf("Strong collision resistance is easier to break than weak collision resistance.\n");
    }

    return 0;
}
