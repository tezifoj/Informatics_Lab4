with open(r"Инф4.Dictionary.txt", "r", encoding="utf-8") as f:
    text = f.read()

import ast
import json

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
print(hcl_result)

