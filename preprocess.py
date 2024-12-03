import csv

input_file = "Denver_Crime(CSCI403).csv"
output_file = "CLEANED_Denver_Crime.csv"
N_COLUMNS = 23
INCIDENT_COLS = [1, 9, 10, 19, 20]
OFFENSE_COLS = [2, 3, 4, 5, 6, 7, 8, ]
LOCATION_COLS = [13, 14, 15, 16, 17, 21, 22]

# with open(input_file, 'r') as input, open(output_file, 'w', newline='') as output:
#   reader = csv.reader(input)
#   writer = csv.writer(output)

#   for row in reader:
#     while len(row) < N_COLUMNS:
#       row.append('')

#     writer.writerow(row)

with open("CLEANED_Denver_Crime.csv", 'r') as input, open("./incident.csv", 'w', newline='') as incident, open("offense.csv", 'w', newline='') as offense, open("location.csv", 'w', newline='') as location:
  reader = csv.reader(input)
  inciWriter = csv.writer(incident)
  offWriter = csv.writer(offense)
  locWriter = csv.writer(location)

  for row in reader:
    idx = 0
    incidentRow = []
    offenseRow = []
    locationRow = []
    for col in row:
      if idx in INCIDENT_COLS:
        incidentRow.append(col)
      elif idx in OFFENSE_COLS:
        offenseRow.append(col)
      elif idx in LOCATION_COLS:
        locationRow.append(col)
      idx += 1
    inciWriter.writerow(incidentRow)
    offWriter.writerow(offenseRow)
    locWriter.writerow(locationRow)
