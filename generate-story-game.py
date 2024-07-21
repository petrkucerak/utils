
input_file = "story-game.txt"

# Load file

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
    # Load keys from header line
    keys = lines[0].replace("\n", "").split("\t")
    lines.pop(0)

    # Load values
    data = []
    for line in lines:
        line = line.replace("\n", "").split("\t")

        card_data = {}
        for i in range(len(keys)):
            card_data[keys[i]] = line[i]

        data.append(card_data)
    print(data)
