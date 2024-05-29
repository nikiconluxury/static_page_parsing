import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os

##DO NOT EDIT OR ADD
class WebsiteParser:
    def __init__(self):
        self.session = requests.Session()

    def read_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def convert_to_tsv(self, data):
        output = []
        for row in data:
            output.append([str(item) for item in row])

        return output

    def write_to_tsv(self, file_path, tsv_data):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(tsv_data)
    def write_to_csv(self, csv_data):
        current_date = datetime.datetime.now().strftime("%d_%m_%Y")
        file_path = f'{self.directory}/{self.brand}_output_{current_date}.csv'

        # Write data to CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(csv_data)
        print(f"Data saved to '{file_path}'")

    def parse_directory(self, directory_path):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt') or f.endswith('.html')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt') or filename.endswith('.html'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    tsv_output[0].append('filename')  # Add the new column name for filename
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to CSV file...")
        self.write_to_csv(all_data)

        return all_data

    def parse_website(self, source, category):
        html_content = self.read_from_file(source)
        soup = BeautifulSoup(html_content, 'html.parser')
        parsed_data = self.parse_product_blocks(soup, category)
        return self.convert_to_tsv(parsed_data)