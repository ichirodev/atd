import re

def remove_invalid_chars(str):
    invalid_chars = "|?_-*"
    for char in invalid_chars:
        str = str.replace(char, "")
    return str

def remove_accent_marks(str):
    accent_marks = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'E': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
    for accent in accent_marks:
        if accent in str:
            str = str.replace(accent, accent_marks[accent])
    return str

def clean_string(str):
    str = remove_invalid_chars(str)
    str = remove_accent_marks(str)
    return str

def find_route(list):
    valid_routes = ['ORAL', 'SUBLINGUAL', 'INYECTABLE', 'RECTAL', 'VAGINAL', 'OCULAR', 
                    'INTRAVENOSA', 'INTRAMUSCULAR', 'INTRALESIONAL', 'INTRAARTICULAR',
                    'OTICA', 'NASAL', 'INHALATORIA', 'CUTANEA']
    for text_line in list:
        if text_line in valid_routes:
            list.remove(text_line)
            return text_line, list
        else:
            for route in valid_routes:
                if route in text_line:
                    list.remove(text_line)
                    return text_line, list
    return "", list

def find_concentration(list):
    valid_concentration = '^[0-9]+\s*((MG)+|(ML)+|(MMOL)+|(G)+|(U)+)+'
    for text_line in list:
        is_valid = re.search(valid_concentration, text_line)
        if is_valid:
            list.remove(text_line)
            return text_line, list
    return "", list