import sys

# takes in a file as an argument
fileName = sys.argv[1]
# convert binary to decimal
with open(fileName) as f:
    for line in f:
        print(line)
# convert decimal to ascii characters
