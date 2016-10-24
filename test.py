item_file = open("seed_data/u.item")

def open_file(item_file):
    for line in item_file:
        
        line = line.rstrip().split("|")

        return max(line[4], len)

