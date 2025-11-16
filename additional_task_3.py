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
print(xml_output)

