import os
import csv
import argparse

def process_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        print(f"File {file_path} is empty.")
        return

    processed_lines = []

    timestamp = 0
    for line in lines:
        if line.startswith("timestamp"):
            processed_lines.append(line)
            continue

        values = line.strip().split(',')
        if len(values) == 6:
            processed_lines.append(f"{timestamp},{','.join(values)}\n")
            timestamp += 10

    with open(file_path, 'w') as f:
        f.writelines(processed_lines)

def process_files_in_folder(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            process_file(file_path)

def main():
    parser = argparse.ArgumentParser(description='Add timestamps to CSV files in a folder.')
    parser.add_argument('input_folder', type=str, help='Path to the input folder containing CSV files')

    args = parser.parse_args()
    process_files_in_folder(args.input_folder)

if __name__ == "__main__":
    main()
