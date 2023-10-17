import subprocess

def edit_input_file(iteration, coord_file_name):
    input_file_name = f'tc{iteration:04d}.in'
    next_iteration = (iteration) % 100  # Set your range here, based on run_wigner.sh settings
    next_coord_file_name = f'x{next_iteration:04d}.xyz'
    
    #Read intial input file. Make one called tc0000.in and put it in this directory
    with open('tc0000.in', 'r') as initial_input_file:
        initial_content = initial_input_file.readlines()

    #Modify the coordinates line
    for i, line in enumerate(initial_content):
        if line.startswith('coordinates'):
            initial_content[i] = f'coordinates      {next_coord_file_name}\n'
            break

    #Write back the modified content
    with open(input_file_name, 'w') as modified_input_file:
        modified_input_file.writelines(initial_content)

    print(f'Edited {input_file_name} with coordinates {next_coord_file_name}')
    
    output_file_name = f'output_{next_iteration:04d}.out'
    with open(output_file_name, 'w') as output_file:
        subprocess.run(['terachem', input_file_name, output_file_name], stdout=output_file)

def iterate_calculations():
    for iteration in range(100):
        coord_file_name = f'x{iteration:04d}.xyz'
        edit_input_file(iteration, coord_file_name)
        print(f'Processed iteration {iteration}')

if __name__ == "__main__":
    iterate_calculations()
