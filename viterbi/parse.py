import argparse

def parse(fname):
    fwrite = open(fname + "_clean", "w+")
    with open(fname) as f:
        content = f.readlines()
        for s in content:
            clean = s.split(" ", 1)[1]
            fwrite.write(clean)
    fwrite.close()

parser = argparse.ArgumentParser()
parser.add_argument("fname")
args = parser.parse_args()
fname = args.fname
parse(fname)

