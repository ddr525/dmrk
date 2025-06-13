
def toFixed(numObj, digits=3):
    if(numObj >= 500):
        return f"{numObj:.{1}f}"
    else:
        return f"{numObj:.{digits}f}"
        
def toFixed_excel(numObj, digits=3):
    return toFixed(numObj, digits).replace('.', ',')

def split_string(input_string):
    # Разделение строки на основную часть и единицы измерения
    if ',' in input_string:
        parts = input_string.split(',', 1)  # Разделяем только по первому вхождению запятой
        key = parts[0].strip()  # Убираем лишние пробелы
        unit = parts[1].strip()
        return key, unit
    else:
        return input_string, None  # Если запятой нет, возвращаем исходную строку