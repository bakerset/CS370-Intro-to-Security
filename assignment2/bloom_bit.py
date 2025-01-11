#author: Seth Baker

import hashlib
import math
import time
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, item):
        for seed in range(self.hash_count):
            result = self._hash(item, seed)
            self.bit_array[result] = 1

    def check(self, item): #same as bloom_filter
        """Check if an item is possibly in the Bloom Filter."""
        for seed in range(self.hash_count):
            result = self._hash(item, seed)
            if self.bit_array[result] == 0:
                return False 
        return True 
    
    def _hash(self, item, seed):
        """Generate a hash for the item using iterative SHA-256"""
        #initial hash with the item and seed
        combined = f"{item}{seed}".encode()
        hash_result = int(hashlib.sha256(combined).hexdigest(), 16) % self.size

        #use iterative hashing if additional hashes are needed
        for _ in range(1, seed):  #start from 1 since we already did the first hash
            hash_result = int(hashlib.sha256(str(hash_result).encode()).hexdigest(), 16) % self.size
        
        return hash_result

def load_bloom_filter(file_path, bloom_filter):
    """Load passwords into the Bloom Filter from a file."""
    with open(file_path, encoding="ISO-8859-1") as file:
        for line in file:
            bloom_filter.add(line.strip())

def test_bloom_filter(bloom_filter, test_file, rockyou_passwords):
    """Test the Bloom Filter against a list of passwords."""
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    with open(test_file, encoding="ISO-8859-1") as file:
        for line in file:
            password = line.strip()
            in_filter = bloom_filter.check(password)
            is_rockyou = password in rockyou_passwords
            
            if in_filter: 
                if is_rockyou:
                    true_positives += 1
                    print("yes") 
                else:
                    false_positives += 1
                    print("maybe") 
            else:
                if is_rockyou:
                    false_negatives += 1
                    print("no") 
                else:
                    true_negatives += 1
                    print("no") 

    return true_positives, false_positives, true_negatives, false_negatives

def main():
    #start timer to measure total execution time
    total_start_time = time.time()
    
    #same parameters
    num_items = 14344392  #number of passwords in rockyou.txt
    false_positive_rate = 0.01  #1% false positive rate

    #calculate Bloom filter size and hash functions count
    size = -int(num_items * math.log(false_positive_rate) / (math.log(2) ** 2))
    hash_count = int(size / num_items * math.log(2))

    #initialize Bloom Filter
    bloom_filter = BloomFilter(size=size, hash_count=hash_count)

    print("Loading passwords into the Bloom Filter...")
    start_time = time.time()
    
    #loading passwords from rockyou.txt
    load_bloom_filter("rockyou.ISO-8859-1.txt", bloom_filter)
    print("Loading complete in {:.2f} seconds.".format(time.time() - start_time))

    #create a reference set of rockyou passwords
    rockyou_passwords = set()
    with open("rockyou.ISO-8859-1.txt", encoding="ISO-8859-1") as file:
        for line in file:
            rockyou_passwords.add(line.strip())

    #test dictionary passwords
    print("Testing dictionary passwords...")
    tp, fp, tn, fn = test_bloom_filter(bloom_filter, "dictionary.txt", rockyou_passwords)

    print("\nStatistics:")
    print("True Positives:", tp)
    print("False Positives:", fp)
    print("True Negatives:", tn)
    print("False Negatives:", fn)

    #same as before
    projected_fp_rate = (1 - math.exp(-hash_count * num_items / size)) ** hash_count
    print("Projected False Positive Rate: {:.2%}".format(projected_fp_rate))
    
    total_tests = tp + fp + tn + fn
    actual_fp_rate = fp / total_tests if total_tests > 0 else 0
    print("Actual False Positive Rate: {:.2%}".format(actual_fp_rate))

    #end timer - same as previous program
    total_time = time.time() - total_start_time
    print("Total execution time: {:.2f} seconds.".format(total_time))

if __name__ == "__main__":
    main()
