#author: Seth Baker

import hashlib
import math
import time

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def add(self, item):
        for seed in range(self.hash_count):
            result = self._hash(item, seed)
            self.bit_array[result] = 1

    def check(self, item):
        """Check if an item is possibly in the Bloom Filter."""
        for seed in range(self.hash_count):
            result = self._hash(item, seed)
            if self.bit_array[result] == 0:
                return False  # false/definitely not in the set
        return True  #if in the set

    def _hash(self, item, seed):
        """Generate a hash for the item using MD5."""
        hash_obj = hashlib.md5(item.encode('utf-8') + str(seed).encode('utf-8')) #using MD5 to generate hash
        return int(hash_obj.hexdigest(), 16) % self.size

def load_bloom_filter(file_path, bloom_filter, num_items):
    """Load up to num_items passwords into the Bloom Filter from a file."""
    with open(file_path, encoding="ISO-8859-1") as file:
        for i, line in enumerate(file):
            if i >= num_items:  #stop loading after num_items entries
                break
            bloom_filter.add(line.strip())

def test_bloom_filter(bloom_filter, test_file, rockyou_passwords):
    """Test the Bloom Filter against a list of passwords.""" #this tests the bloom filters and tracks statistics
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    with open(test_file, encoding="ISO-8859-1") as file:
        for line in file:
            password = line.strip()
            in_filter = bloom_filter.check(password)
            is_rockyou = password in rockyou_passwords
            
            if in_filter:  #the password may be in the Bloom Filter
                if is_rockyou:
                    true_positives += 1
                    print("yes")  # "yes" the password is in rockyou
                else:
                    false_positives += 1
                    print("maybe")  # "maybe" the password is in the Bloom Filter, but not in rockyou
            else:
                if is_rockyou:
                    false_negatives += 1
                    print("no")  # "no" the password is not in the Bloom Filter but is in rockyou
                else:
                    true_negatives += 1
                    print("no")  # "no" the password is not in either

    return true_positives, false_positives, true_negatives, false_negatives

def main():
    total_start_time = time.time()
    
    #parameters
    num_items = 20000  # Number of passwords in rockyou.txt - limit to 20,000
    false_positive_rate = 0.01  # 1% false positive rate

    size = -int(num_items * math.log(false_positive_rate) / (math.log(2) ** 2))
    hash_count = int(size / num_items * math.log(2))

    bloom_filter = BloomFilter(size=size, hash_count=hash_count)

    print("Loading passwords into the Bloom Filter...")
    start_time = time.time()

    load_bloom_filter("rockyou.ISO-8859-1.txt", bloom_filter, num_items)
    print("Loading complete in {:.2f} seconds.".format(time.time() - start_time))

    #create a reference set of rockyou passwords (limited to num_items)
    rockyou_passwords = set()
    with open("rockyou.ISO-8859-1.txt", encoding="ISO-8859-1") as file:
        for i, line in enumerate(file):
            if i >= num_items:  #stop after num_items
                break
            rockyou_passwords.add(line.strip())

    #test dictionary passwords
    print("Testing dictionary passwords...")
    tp, fp, tn, fn = test_bloom_filter(bloom_filter, "dictionary.txt", rockyou_passwords)

    print("\nStatistics:")
    print("True Positives:", tp)
    print("False Positives:", fp)
    print("True Negatives:", tn)
    print("False Negatives:", fn)

    projected_fp_rate = (1 - math.exp(-hash_count * num_items / size)) ** hash_count
    print("Projected False Positive Rate: {:.2%}".format(projected_fp_rate))
    
    total_tests = tp + fp + tn + fn
    actual_fp_rate = fp / total_tests if total_tests > 0 else 0
    print("Actual False Positive Rate: {:.2%}".format(actual_fp_rate))

    total_time = time.time() - total_start_time
    print("Total execution time: {:.2f} seconds.".format(total_time))

if __name__ == "__main__":
    main()
