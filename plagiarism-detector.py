#!/usr/bin/python3

import os       # Used for creating directories and handling file paths
import string   # Used for punctuation removal during text cleaning

# -------------------------------
# 1. Text Processing Function
# -------------------------------
def process_text(file_path):
    """
    Reads a text file, cleans it, and returns a list of meaningful words.
    Cleaning steps:
    - Convert text to lowercase
    - Remove punctuation
    - Split into words
    - Remove stop words
    """
    stop_words = {'a', 'an', 'the', 'is', 'in', 'of', 'and', 'to', 'for', 'on', 'with'}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        # Error handling: if file is missing, return empty list
        print(f"Error: File {file_path} not found.")
        return []

    # Convert all text to lowercase for uniformity
    text = text.lower()

    # Remove punctuation (commas, periods, etc.)
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Split text into individual words
    words = text.split()

    # Remove stop words (common words with little meaning)
    clean_words = [word for word in words if word not in stop_words]

    return clean_words


# -------------------------------
# 2. Word Search Function
# -------------------------------
def word_search(word, essay1_words, essay2_words):
    """
    Counts how many times a given word appears in each essay.
    """
    count1 = essay1_words.count(word.lower())
    count2 = essay2_words.count(word.lower())
    return count1, count2


# -------------------------------
# 3. Common Words Report
# -------------------------------
def common_words(essay1_words, essay2_words):
    """
    Finds and returns the set of words that appear in both essays.
    """
    return set(essay1_words).intersection(set(essay2_words))


# -------------------------------
# 4. Plagiarism Calculation
# -------------------------------
def plagiarism_check(essay1_words, essay2_words):
    """
    Calculates plagiarism percentage using Jaccard Similarity:
    (Intersection / Union) * 100
    Also prints common words and optionally saves them to a report file.
    """
    set1 = set(essay1_words)
    set2 = set(essay2_words)

    # Intersection = words common to both essays
    intersection = set1.intersection(set2)
    # Union = all unique words across both essays
    union = set1.union(set2)

    # Avoid division by zero if both essays are empty
    if len(union) == 0:
        similarity = 0
    else:
        similarity = (len(intersection) / len(union)) * 100

    # Display plagiarism percentage
    print(f"\nPlagiarism Percentage: {similarity:.2f}%")
    if similarity >= 50:
        print("⚠️ Similarity is likely.")
    else:
        print("✅ Similarity is low.")

    # Show common words
    print("\nCommon Words:")
    print(intersection)

    # Ask user if they want to save report
    choice = input("\nDo you want to save this report? (y/n): ").strip().lower()
    if choice == 'y':
        os.makedirs("reports", exist_ok=True)  # Ensure reports folder exists
        with open("reports/similarity_report.txt", "w", encoding="utf-8") as f:
            f.write("Common Words:\n")
            f.write(", ".join(intersection))
        print("Report saved to reports/similarity_report.txt")


# -------------------------------
# Main Program
# -------------------------------
def main():
    """
    Main driver function:
    - Processes both essays
    - Allows user to search for a word
    - Displays common words
    - Calculates plagiarism percentage
    """
    essay1_words = process_text("essays/essay1.txt")
    essay2_words = process_text("essays/essay2.txt")

    # If either essay could not be processed, stop execution
    if not essay1_words or not essay2_words:
        print("Error: One or both essays could not be processed.")
        return

    # Word Search Feature
    search_word = input("\nEnter a word to search: ").strip().lower()
    if search_word:  # Validate input is not empty
        count1, count2 = word_search(search_word, essay1_words, essay2_words)
        print(f"'{search_word}' appears {count1} times in essay1 and {count2} times in essay2.")
    else:
        print("No word entered. Skipping word search.")

    # Common Words Report
    common = common_words(essay1_words, essay2_words)
    print("\nCommon Words Report:")
    print(common)

    # Plagiarism Check
    plagiarism_check(essay1_words, essay2_words)


# Run the program
if __name__ == "__main__":
    main()

