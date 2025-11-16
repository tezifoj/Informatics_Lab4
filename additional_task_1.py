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
print(hcl_output)
