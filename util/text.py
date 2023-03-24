import re

def remove_invalid_chars(str):
    invalid_chars = "|?_-*/\\'"
    for char in invalid_chars:
        str = str.replace(char, "")
    return str

def remove_quotes(str):
    str = str.replace("\'", "")
    str = str.replace("\"", "")
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

def find_first(list, dictionary):
    for text_line in list:
        if text_line in dictionary:
            list.remove(text_line)
            return text_line, list
        else:
            for word in dictionary:
                if word in text_line:
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

def filter_text(list, dictionary):
    for text_line in list:
        if text_line in dictionary:
            list.remove(text_line)
    
    for word in dictionary:
        for text_line in list:
            if word in text_line:
                list.remove(text_line)

    for text_line in list:
        if len(text_line) <= 3:
            list.remove(text_line)
    
    return list