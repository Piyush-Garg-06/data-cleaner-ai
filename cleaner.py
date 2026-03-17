import json

# Function to convert word numbers to integers
def word_to_number(word):
    word = word.lower()
    mapping = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19,
        "twenty": 20
    }

    if "-" in word:
        parts = word.split("-")
        return mapping.get(parts[0], 0) + mapping.get(parts[1], 0)
    
    return mapping.get(word, 0)


cleaned_data = []

with open("messyData.txt", "r") as file:
    for line in file:
        parts = line.strip().split("|")

        data = {}
        for part in parts:
            key, value = part.split(":")
            key = key.strip().lower()
            value = value.strip()

            if key == "name":
                # Proper capitalization
                data["name"] = " ".join(word.capitalize() for word in value.split())

            elif key == "email":
                data["email"] = value.lower()

            elif key == "age":
                # Convert to integer
                if value.isdigit():
                    data["age"] = int(value)
                else:
                    data["age"] = word_to_number(value)

        cleaned_data.append(data)

# Write to JSON file
with open("clean_data.json", "w") as outfile:
    json.dump(cleaned_data, outfile, indent=4)

print("Data cleaned and saved to clean_data.json ✅")