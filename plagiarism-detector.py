import os
import string

# 1. Text Processing Function
def process_text(file_path):
    stop_words = {'a', 'an', 'the', 'is', 'in', 'of', 'and', 'to', 'for', 'on', 'with'}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    clean_words = [word for word in words if word not in stop_words]
    return clean_words

# 2. Word Search
def word_search(word, essay1_words, essay2_words):
    count1 = essay1_words.count(word.lower())
    count2 = essay2_words.count(word.lower())
    return count1, count2

# 3. Common Words Report
def common_words(essay1_words, essay2_words):
    return set(essay1_words).intersection(set(essay2_words))

# 4. Plagiarism Calculation
def plagiarism_check(essay1_words, essay2_words):
    set1 = set(essay1_words)
    set2 = set(essay2_words)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    similarity = (len(intersection) / len(union)) * 100 if union else 0

    print(f"\nPlagiarism Percentage: {similarity:.2f}%")
    if similarity >= 50:
        print("⚠️ Similarity is likely.")
    else:
        print("✅ Similarity is low.")

    print("\nCommon Words:")
    print(intersection)

    choice = input("\nDo you want to save this report? (y/n): ").strip().lower()
    if choice == 'y':
        os.makedirs("reports", exist_ok=True)
        with open("reports/similarity_report.txt", "w", encoding="utf-8") as f:
            f.write("Common Words:\n")
            f.write(", ".join(intersection))
        print("Report saved to reports/similarity_report.txt")

# Main Program
def main():
    essay1_words = process_text("essays/essay1.txt")
    essay2_words = process_text("essays/essay2.txt")

    if not essay1_words or not essay2_words:
        print("Error: One or both essays could not be processed.")
        return

    search_word = input("\nEnter a word to search: ").strip().lower()
    if search_word:
        count1, count2 = word_search(search_word, essay1_words, essay2_words)
        print(f"'{search_word}' appears {count1} times in essay1 and {count2} times in essay2.")
    else:
        print("No word entered. Skipping word search.")

    print("\nCommon Words Report:")
    print(common_words(essay1_words, essay2_words))

    plagiarism_check(essay1_words, essay2_words)

if __name__ == "__main__":
    main()
