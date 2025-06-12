
def print_splited_content(filename):
    with open(filename, "r") as file:
        line = file.readline()
        if not line:
            return
        for digit in line.split(','):
            print(digit)

if __name__ == "__main__":
    filename = "numbers.txt"
    print_splited_content(filename)