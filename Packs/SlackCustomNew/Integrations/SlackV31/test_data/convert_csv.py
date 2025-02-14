import csv

# Define the input CSV file and output JSON file
csv_file = '/Users/hnguyen/Google_Drive/XSOAR-Dev/local-dev/content/Packs/SlackCustomNew/Integrations/SlackV31/test_data/input.csv'

# Read the CSV file and convert it to a list of dictionaries
data = []
with open(csv_file, 'r') as csv_file:
    print(csv_file)
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

print(data)