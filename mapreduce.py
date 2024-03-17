import os
from collections import Counter, defaultdict

# Function to read records from a node file
def read_records_from_node(node_filename):
    with open(node_filename, 'r') as file:
        lines = file.readlines()
    return [(i+1, line.strip()) for i, line in enumerate(lines)]

# Function to perform mapping
def mapper(records):
    word_frequencies = []
    for _, sentence in records:
        words = sentence.lower().split()
        frequencies = Counter(words)
        word_frequencies.extend(frequencies.items())
    return word_frequencies

# Function to perform shuffling and sorting
def shuffle_and_sort(mapper_outputs):
    shuffle_sort_output = defaultdict(list)
    for word, frequency in mapper_outputs:
        shuffle_sort_output[word].append(frequency)
    return shuffle_sort_output

# Function to perform reducing
def reducer(shuffle_sort_output):
    reduced_output = {}
    for word, frequencies in shuffle_sort_output.items():
        total_count = sum(frequencies)
        reduced_output[word] = total_count
    return reduced_output

# Function to split the input file into smaller parts
def split_file(input_file, num_chunks):
    """
    Splits the input file into smaller parts.
    
    :param input_file: Path to the input file.
    :param num_chunks: Number of parts to split the file into.
    :return: List of paths to the split files.
    """
    split_files = []
    with open(input_file, 'r') as file:
        # Get the total number of lines in the file
        total_lines = sum(1 for line in file)
        lines_per_chunk = total_lines // num_chunks
        file.seek(0)  # Reset file pointer to the beginning
        for i in range(num_chunks):
            chunk_file = f'node_{i+1}.txt'
            split_files.append(chunk_file)
            with open(chunk_file, 'w') as chunk:
                # Write lines_per_chunk lines to each chunk
                for _ in range(lines_per_chunk):
                    chunk.write(file.readline())
    return split_files

# Function to merge reduced outputs from all nodes
def merge_reduced_outputs(reduced_files):
    merged_output = defaultdict(int)
    for filename in reduced_files:
        with open(filename, 'r') as file:
            for line in file:
                word, count = line.strip().split('\t')
                merged_output[word] += int(count)
    return merged_output

# Main process
if __name__ == "__main__":
    # File path to the text file to split
    input_file = 'large_text_file.txt'
    # Number of parts to split the file into
    num_chunks = 3
    
    # Split the input file into parts
    split_files = split_file(input_file, num_chunks)
    print(f"File '{input_file}' split into {num_chunks} parts:")
    for file in split_files:
        print(file)

    # Process each split file
    reduced_files = []
    for node_filename in split_files:
        records = read_records_from_node(node_filename)
        # Map step
        node_word_frequencies = mapper(records)
        # Shuffle and sort step
        node_shuffled_output = shuffle_and_sort(node_word_frequencies)
        # Reduce step
        node_reduced_output = reducer(node_shuffled_output)
        # Write the reduced output to a file
        reduced_filename = f"{node_filename.split('.')[0]}_reduced.txt"
        with open(reduced_filename, 'w') as file:
            for word, count in node_reduced_output.items():
                file.write(f"{word}\t{count}\n")
        reduced_files.append(reduced_filename)
        # For demonstration, print some of the reduced output
        print(f"Reduced output from {node_filename}:")
        for word, count in list(node_reduced_output.items())[:5]:  # Limiting output for brevity
            print(f"{word}: {count}")
        print("\n---\n")  # Just to separate output for clarity
    
    # Merge reduced outputs from all nodes
    merged_output = merge_reduced_outputs(reduced_files)
    
    # Write the merged output to a file
    merged_output_file = 'merged_word_counts.txt'
    with open(merged_output_file, 'w') as file:
        for word, count in sorted(merged_output.items()):
            file.write(f"{word}\t{count}\n")
    
    # Print the values of the merged output file
    print("Values of merged output file:")
    with open(merged_output_file, 'r') as file:
        for line in file:
            print(line.strip())