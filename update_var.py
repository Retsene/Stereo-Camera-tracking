def update_var(var: str, val: str):
    path = 'variables.txt'
    updated_lines = []
    with open(path, 'r') as file:
        for line in file:
            if line.startswith(var):
                updated_lines.append(f"{var}: {val}\n")  
            else:
                updated_lines.append(line)

# Write the updated lines back to the file
    with open(path, 'w') as file:
        file.writelines(updated_lines)
     
