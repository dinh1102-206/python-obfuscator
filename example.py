import sys
import math

def calculate_stats(numbers):
    n = len(numbers)
    if n == 0:
        return 0, 0
    mean = sum(numbers) / n
    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = math.sqrt(variance)
    return mean, std_dev

def main():
    data = [12, 15, 23, 42, 56, 78, 99]
    avg, sd = calculate_stats(data)
    print("=== Statistical Analysis ===")
    print(f"Dataset: {data}")
    print(f"Average: {avg:.2f}")
    print(f"Standard Deviation: {sd:.2f}")
    print("Status: Success!")

if __name__ == "__main__":
    main()
