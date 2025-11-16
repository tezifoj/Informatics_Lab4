import tomllib

with open("Инф4.toml", "rb") as f:
    data = tomllib.load(f)
print(data)

