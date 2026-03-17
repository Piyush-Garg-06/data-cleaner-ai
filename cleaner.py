import json
import difflib
import re
import os

# Valid keys
VALID_KEYS = ["name", "age", "email"]

# Fuzzy key mapping
def map_key(raw_key):
    raw_key = raw_key.lower().strip()
    match = difflib.get_close_matches(raw_key, VALID_KEYS, n=1, cutoff=0.6)
    return match[0] if match else None

# Convert word numbers to integer
def word_to_number(text):
    text = text.lower().strip()

    mapping = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19,
        "twenty": 20, "thirty": 30, "forty": 40
    }

    # Split on space OR hyphen
    parts = re.split(r"[ -]", text)

    total = 0
    for part in parts:
        if part in mapping:
            total += mapping[part]

    return total if total > 0 else None


cleaned_data = []

try:
    # Ensure correct file path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "messyData.txt")
    output_path = os.path.join(base_dir, "clean_data.json")

    print("Reading from:", input_path)

    with open(input_path, "r") as file:
        for line in file:
            parts = line.strip().split("|")
            data = {}

            for part in parts:
                if ":" not in part:
                    continue

                raw_key, value = part.split(":", 1)
                key = map_key(raw_key)

                if not key:
                    continue

                value = value.strip()

                if key == "name":
                    data["name"] = " ".join(word.capitalize() for word in value.split())

                elif key == "email":
                    data["email"] = value.lower()

                elif key == "age":
                    if value.isdigit():
                        data["age"] = int(value)
                    else:
                        num = word_to_number(value)
                        if num is not None:
                            data["age"] = num

            if data:  # avoid empty entries
                cleaned_data.append(data)

    print("Processed Data:", cleaned_data)

    # Write JSON file
    with open(output_path, "w") as outfile:
        json.dump(cleaned_data, outfile, indent=4)

    print("JSON file created at:", output_path)

except Exception as e:
    print("Error:", e)