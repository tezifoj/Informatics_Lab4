import time
import tomllib
import ast
import json


def program1():
    with open(r"Инф4.toml", "r", encoding="utf-8") as f:
        text = f.read()

    def parse_toml(content):
        result = {}
        current_section = result
        lines = content.split('\n')

        for line in lines:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if line.startswith("[") and line.endswith("]"):
                section_path = line[1:-1].split(".")

                current_section = result
                stack = []

                for i in section_path:
                    if i not in current_section:
                        current_section[i] = {}
                    stack.append(current_section)
                    current_section = current_section[i]

            elif "=" in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                if "." in key:
                    one, two = key.split('.', 1)
                    if two not in current_section or not isinstance(current_section[two], dict):
                        current_section[two] = {}

                    current_section[two][one] = parse_value(value)
                else:
                    current_section[key] = parse_value(value)
        return result

    def parse_value(value):
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            return value[1:-1]

        if ':' in value and value.count(':') == 2:
            return value

        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False

        if value.lower() == "null" or value.lower() == "":
            return None

        return value

    parsed_data = parse_toml(text)
    return parsed_data


def program2():
    with open(r"Инф4.Dictionary.txt", "r", encoding="utf-8") as f:
        text = f.read()

    def dict_to_hcl(data, indent=0):
        lines = []
        spaces = " " * indent * 2
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{spaces}{key} {{")
                lines.append(dict_to_hcl(value, indent + 1))
                lines.append(f"{spaces}}}")

            elif isinstance(value, list):
                items = []
                for item in value:
                    if isinstance(item, dict):
                        items.append("{\n" + dict_to_hcl(item, indent + 1) + "}")
                    elif isinstance(item, str):
                        items.append(f"{item}")
                    elif item is None:
                        items.append('null')
                    elif isinstance(item, bool):
                        items.append(str(item).lower())
                    else:
                        items.append(str(item))

            else:
                if isinstance(value, str):
                    lines.append(f'{spaces}{key} = "{value}"')
                elif isinstance(value, bool):
                    lines.append(f"{spaces}{key} = {str(value).lower()}")
                elif isinstance(value, (int, float)):
                    lines.append(f"{spaces}{key} = {value}")
                elif value is None:
                    lines.append(f"{spaces}{key} = null")

        return "\n".join(lines)

    hcl_output = dict_to_hcl(eval(text))
    return hcl_output


def program3():
    with open(r"Инф4.Dictionary.txt", "r", encoding="utf-8") as f:
        text = f.read()

    dictionary = ast.literal_eval(text)

    def to_hcl(data, indent=0):
        spaces = "  " * indent
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                if isinstance(value, dict):
                    lines.append(f"{spaces}{key} {{")
                    lines.append(to_hcl(value, indent + 1))
                    lines.append(f"{spaces}}}")
                else:
                    lines.append(f'{spaces}{key} = {json.dumps(value, ensure_ascii=False)}')
            return "\n".join(lines)
        return json.dumps(data, ensure_ascii=False)

    hcl_result = to_hcl(dictionary)
    return hcl_result


def program4():
    with open("Инф4.toml", "rb") as f:
        data = tomllib.load(f)
    return data


def program5():
    with open(r"Инф4.Dictionary.txt", "r", encoding="utf-8") as f:
        text = f.read()

    def dict_to_xml(data, indent=0):
        lines = []
        spaces = " " * indent * 2
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{spaces}<{key}>")
                lines.append(dict_to_xml(value, indent + 1))
                lines.append(f"{spaces}</{key}>")

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f"{spaces}<{key}>")
                        lines.append(dict_to_xml(item, indent + 1))
                        lines.append(f"{spaces}</{key}>")
                    else:
                        item_str = str(item).lower() if isinstance(item, str) else str(item)
                        if item is None:
                            item_str = "null"
                        lines.append(f"{spaces}<{key}>{item_str}</{key}>")

            else:
                if isinstance(value, str):
                    lines.append(f'{spaces}<{key}>{value}</{key}>')
                elif isinstance(value, bool):
                    lines.append(f"{spaces}<{key}>{str(value).lower()}</{key}>")
                elif isinstance(value, (int, float)):
                    lines.append(f"{spaces}<{key}>{value}</{key}>")
                elif value is None:
                    lines.append(f"{spaces}<{key}>null</{key}>")

        return "\n".join(lines)

    xml_output = dict_to_xml(eval(text))
    return xml_output


def test_parsing_and_conversion(program_func, program_name):
    # Измеряет стократное время выполнения парсинга + конвертации
    start_time = time.time()
    for _ in range(100):
        result = program_func()
    execution_time = time.time() - start_time

    print(f"{program_name}: {execution_time:.6f} секунд")


def main():
    programs = [
        (program1, "Программа 1 (парсинг TOML + конвертация в dict)"),
        (program2, "Программа 2 (парсинг Dictionary + конвертация в HCL)"),
        (program3, "Программа 3 (парсинг Dictionary + конвертация в HCL через json)"),
        (program4, "Программа 4 (парсинг TOML через tomllib)"),
        (program5, "Программа 5 (парсинг Dictionary + конвертация в XML)")
    ]

    for program_func, program_name in programs:
        test_parsing_and_conversion(program_func, program_name)

main()