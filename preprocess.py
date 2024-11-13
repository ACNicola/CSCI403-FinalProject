import csv

input_file = "Denver_Crime(CSCI403).csv"
output_file = "CLEANED_Denver_Crime.csv"
N_COLUMNS = 23

with open(input_file, 'r') as input, open(output_file, 'w', newline='') as output:
  reader = csv.reader(input)
  writer = csv.writer(output)

  for row in reader:
    while len(row) < N_COLUMNS:
      row.append('')

    writer.writerow(row)