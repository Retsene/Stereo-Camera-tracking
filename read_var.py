def read_var(var_name: str):
    path = "variables.txt"
    with open(path, 'r') as file:
        for line in file:
            # Check if the line starts with the variable name
            if line.startswith(f"{var_name}:"):
                # Extract the value after the colon
                value = line.split(":", 1)[1].strip()
                # Check if it's a tuple
                if value.startswith("(") and value.endswith(")"):
                    return tuple(map(int, value.strip("()").split(",")))
                # Otherwise, assume it's an integer
                else:
                    return int(value)
    # If the variable is not found, raise an error
    raise ValueError(f"Variable '{var_name}' not found in file.")


