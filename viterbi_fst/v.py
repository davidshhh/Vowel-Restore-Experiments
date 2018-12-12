import argparse

# strip vowels off
vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
def strip_vowels(w):
    nv_w = ''.join([l for l in w if l not in vowels])
    if not nv_w:
        nv_w = w
    return nv_w

def build_vocab(vocab):
    with open(vocab) as f:
        vocab_dict = {}
        content = f.readlines()
        for w in content:
            w = w.strip()
            w_nv = strip_vowels(w)
            if w_nv not in vocab_dict:
                vocab_dict[w_nv] = [w]
            else:
                vocab_dict[w_nv].append(w)
    
        isyms = open('unvowelized.txt', 'w')
        osyms = open('vowelized.txt', 'w')
        text = open('v.text', 'w')
        n = 3;
        c = 3;
        isyms.write("<eps> 0\n")
        isyms.write("<s> 1\n")
        isyms.write("</s> 2\n")
        osyms.write("<eps> 0\n")
        osyms.write("<s> 1\n")
        osyms.write("</s> 2\n")
        
        for k in vocab_dict:
            isyms.write(k + " " + str(c) + "\n")
            c += 1
            for v in vocab_dict[k]:
                osyms.write(v + " " + str(n) + "\n")
                n += 1
                text.write("0 0 " + k + " " + v + " 0\n")
        text.write("0 0")
                
        isyms.close()
        osyms.close()
        text.close()
        return n - 1
        
parser = argparse.ArgumentParser()
parser.add_argument("vocab")

args = parser.parse_args()
vocab = args.vocab

n = build_vocab(vocab)
print n
