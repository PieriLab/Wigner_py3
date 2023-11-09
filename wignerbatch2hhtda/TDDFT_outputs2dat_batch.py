#Written by Gregory Curtin
import re
import sys

default_num_files = 100

#Allows you to insert an argunemt when running the code about the number of wigner sample files
if len(sys.argv) > 1:
    try:
        Total_files = int(sys.argv[1])
    except ValueError:
        print("Invalid input for total number of files. Using default value of 100.")
        Total_files = default_num_files

# Define the names of the columns to extract
column_names = ["Energy (eV)", "Osc. (a.u.)"]

# Initialize empty lists to store the extracted data
batch_energy = []
batch_oscillator_strength = []

# Specify the path and name of your results file
file_to_print = './TDDFT_batch_results.dat'

for file_index in range(Total_files):
    #Change range based on how many 
    file_to_read = f'./output_{file_index:04d}.out'

    # Initialize empty lists to store the extracted data
    energy = []
    oscillator_strength = []

    lines_to_skip = 0
    extract_table = False

    numeric_values_pattern = re.compile(r'(-?\d+\.\d+)')

    with open(file_to_read, 'r') as input:
        for line in input:
            if lines_to_skip > 0:
                print("Skipping line:", repr(line))
                lines_to_skip -= 1
                continue

            if "Final Excited State Results:" in line:
                print("Found header line:", repr(line))
                extract_table = True
                lines_to_skip = 3
                continue  
    
            if extract_table:
                parts = line.split()

                # Check if the line contains the expected number of numeric values
                if len(parts) >= 7:
                    # Extract values for the specified columns
                    energy.append(float(parts[2]))
                    oscillator_strength.append(float(parts[3])) 
            
                else:
                    # If the line doesn't have the expected number of columns, stop extracting
                    extract_table = False
                    break
           
    batch_energy.append(energy)
    batch_oscillator_strength.append(oscillator_strength)

# Debugging print statements
print("Energy:", energy)
print("Oscillator Strength:", oscillator_strength)

with open(file_to_print, 'w') as output:
    # Write header
    #output.write("File Index\t") This was for benchmarking, please ignore
    for i in range(Total_files):
        output.write(f"geom{i}\tO{i}\t")
    output.write("\n") 

    for row_index in range(max(len(row) for row in batch_energy)):
        #output.write(f"{row_index}\t") same thing, for benchmarking purpose, please ignore
        for col_index in range(Total_files):
            if row_index < len(batch_energy[col_index]):
                output.write(f"{batch_energy[col_index][row_index]}\t{batch_oscillator_strength[col_index][row_index]}\t")
            else:
                output.write("\t\t")

        output.write("\n")

print("Data extracted and saved to:", file_to_print)

transformed_file = 'transformed_TDDFT_batch_results.dat'

# Initialize empty lists to store the merged even and odd column data
merged_even_columns = []
merged_odd_columns = []

# Read the original data, skipping the header
with open(file_to_print, 'r') as infile:
    next(infile)  # Skip the header line
    for line in infile:
        # Split the line into columns
        columns = line.strip().split('\t')
        # Process even and odd indexed columns
        for i, value in enumerate(columns):
            if i % 2 == 0:  # Even indexed columns (including 0)
                merged_even_columns.append(value)
            else:  # Odd indexed columns
                merged_odd_columns.append(value)

# Now we write the merged columns into the new file
with open(transformed_file, 'w') as outfile:
    outfile.write("Even_Indexed_Columns\tOdd_Indexed_Columns\n")
    for even, odd in zip(merged_even_columns, merged_odd_columns):
        outfile.write(f"{even}\t{odd}\n")

print(f"Data transformed and saved to: {transformed_file}")

formatted_file = 'formatted_TDDFT_batch_results.dat'

def_max_column_pairs = 5

if len(sys.argv) > 1:
    try:
        max_column_pairs  = int(sys.argv[2])
    except ValueError:
        print("Invalid input for total number of states. Using default value of 5.")
        max_column_pairs = def_max_column_pairs
else:
    max_column_pairs = def_max_column_pairs

lines = []

# Read the original transformed data
with open(transformed_file, 'r') as infile:
         lines = infile.readlines()[1:]  # skip header line

# Prepare the data, split lines into two columns, and strip to remove whitespace/newlines
data_pairs = [line.strip().split('\t') for line in lines]

# Calculate the number of rows for the new format
num_rows = Total_files
#if len(data_pairs) % 3:
    #num_rows += 1  # Add an extra row if there are remaining lines

# Limit the number of columns to the set maximum, if necessary
num_columns = max_column_pairs * 2

# Prepare the header for the new file
headers = [f's{col // 2 + 1}' if col % 2 == 0 else f'o{col // 2 + 1}' for col in range(num_columns)]

# Write the transformed data to the new file
with open(formatted_file, 'w') as outfile:
    # Write the header row
    outfile.write('\t'.join(headers) + '\n')

    # Write the reformatted data by joining three rows at a time, limited by max_column_pairs
    for row_idx in range(num_rows):
        row = []
        for col_idx in range(0, num_columns * max_column_pairs, max_column_pairs * 2):  # Step by double to process pairs of 's' and 'o'
            if row_idx + col_idx // 2 < len(data_pairs):
                row.extend(data_pairs[row_idx + col_idx // 2])
            else:
                row.extend(['', ''])  # Add empty strings if there is no data
        outfile.write('\t'.join(row) + '\n')

print(f"Data formatted and saved to: {formatted_file}")
