import random
import lorem

# Function to generate a random sentence
def generate_sentence():
    return lorem.sentence()

# Function to generate a large text file
def generate_text_file(file_path, num_sentences):
    with open(file_path, 'w') as f:
        for _ in range(num_sentences):
            sentence = generate_sentence()
            f.write(sentence + '\n')

if __name__ == "__main__":
    file_path = "large_text_file.txt"
    num_sentences = 1000  # Adjust the number of sentences to generate a file of desired size
    generate_text_file(file_path, num_sentences)
    print(f"Generated a text file at '{file_path}' with {num_sentences} sentences.")
