from collections import defaultdict

def IndexPrinter(title, index, filecounter, dirpath):

    name = dirpath + "index" + str(filecounter) + ".txt"
    file = open(name, "w")
    
    titler = "titles/" + str(filecounter) + ".txt"
    titlefile = open(titler, 'w')

    with open(name, 'w') as file:
        for i in sorted(index.keys()):
            s = i + ":"
            posting = index[i]
            s += " ".join(posting)
            file.write(s + "\n")
    
    with open(titler, 'w') as file:
        for i in title:
            posting = i
            # s = " ".join(posting)
            i = i.lower()
            print(i)
            titlefile.write(i + "\n")

    index = defaultdict(list)
    print("created file", filecounter)
    filecounter += 1
    return title, index, filecounter