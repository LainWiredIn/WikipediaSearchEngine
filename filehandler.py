from collections import defaultdict

def IndexPrinter(index, filecounter, dirpath):

    name = dirpath + "index" + str(filecounter) + ".txt"
    file = open(name, "w")

    with open(name, 'w') as file:
        for i in sorted(index.keys()):
            s = i + ":"
            posting = index[i]
            s += " ".join(posting)
            file.write(s + "\n")

    index = defaultdict(list)
    print("created file", filecounter)
    filecounter += 1
    return index, filecounter