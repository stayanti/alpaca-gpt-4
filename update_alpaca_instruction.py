import os
import json
import random
from pathlib import Path

def select_random_file(dir_path):
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    return random.choice(files) if files else None

def main():
    alpaca_data_path = 'alpaca_data'
    alpaca_data_gpt4_path = 'alpaca_data_gpt4'

    # Create alpaca_data_gpt4 folder if not exists
    Path(alpaca_data_gpt4_path).mkdir(parents=True, exist_ok=True)

    random_file = select_random_file(alpaca_data_path)
    
    if random_file:
        with open(os.path.join(alpaca_data_path, random_file), 'r') as file:
            data = json.load(file)

        while data:
            entry = data.pop(0)

            print("######## Instruction ########")
            print(f"{entry['instruction']}")
            print("######## Input ########")
            print(f"{entry['input']}")
            print("######## Previous Output ########")
            print(f"{entry['output']}\n")

            print("######## INSTRUCTION FOR GPT4 ########")
            print("Respond to the given instruction and input with a suitable answer, ensuring it is concise and under 100 words. Refrain from using line breaks or code examples.")
            print(f"Instruction: {entry['instruction']}")
            print(f"Input: {entry['input']}\n")

            print("######## Copy the gpt output here, if the entire instruction is invalid leave an empty response ########")
            entry['new_response']  = input("Enter your new response:")

            # Update the old file
            with open(os.path.join(alpaca_data_path, random_file), 'w') as outfile:
                json.dump(data, outfile, indent=2)

            # If there are no entries left in the old file, delete it
            if not data:
                os.remove(os.path.join(alpaca_data_path, random_file))

            # Load the entries from the new file, if it exists
            try:
                with open(os.path.join(alpaca_data_gpt4_path, random_file), 'r') as infile:
                    new_data = json.load(infile)
            except FileNotFoundError:
                new_data = []

            # Append the entry with the new response to the new file
            new_data.append(entry)

            with open(os.path.join(alpaca_data_gpt4_path, random_file), 'w') as outfile:
                json.dump(new_data, outfile, indent=2)
    else:
        print("No files found in alpaca_data folder.")

if __name__ == '__main__':
    main()
