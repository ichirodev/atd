def load_dictionary(file_path):
    lines = []
    with open(file_path) as file_dictionary:
        for line in file_dictionary:
            lines.append(line.replace('\n', ''))
    return lines