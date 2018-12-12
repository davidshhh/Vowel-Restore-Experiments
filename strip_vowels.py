import argparse

def parse(fname):
    fwrite = open(fname + "_nv", "w+")
    vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
    with open(fname) as f:
        content = f.readlines()
        for s in content:
            words = s.split();
            for w in words:
                nv_w = ''.join([l for l in w if l not in vowels])
                if not nv_w:
                    nv_w = w
                fwrite.write(nv_w + " ")
            fwrite.write("\n")
                
        fwrite.close()

parser = argparse.ArgumentParser()
parser.add_argument("fname")
args = parser.parse_args()
fname = args.fname
parse(fname)

