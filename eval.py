import argparse
import operator

print_sort = False
print_lines = False

def compare(text_ori, text_cured):
    dup = {}
    with open(text_ori) as to, open(text_cured) as tc:
        count = 0
        correct = 0
        for lo, lc in zip(to, tc):
            wordso = lo.split();
            wordsc = lc.split();
            not_printed = True
            for wo, wc in zip(wordso, wordsc):
                if wo == wc:
                    correct += 1
                else:
                    if print_lines and not_printed:
                        not_printed = False
                        print lo,
                    if (wo, wc) in dup:
                        dup[(wo, wc)] += 1
                    else:
                        dup[(wo, wc)] = 1
                count += 1

        sorted_dup = sorted(dup.items() ,key=operator.itemgetter(1))
        if print_sort:
            for k in sorted_dup:
                print k
        print str(correct / float(count) * 100) + "% (" + str(correct) + "/" + str(count) + ")of words were correctly vowelized"

parser = argparse.ArgumentParser()
parser.add_argument("text_ori");
parser.add_argument("text_cured");
parser.add_argument("-d", "--diff", action="store_true",
                    help = "print lines that contains incorrectly vowelized words, in order of text");
parser.add_argument("-s", "--sort", action="store_true",
                    help="print words that were incorrectly vowelized, sorted by occurences");
args = parser.parse_args()
text_ori = args.text_ori
text_cured = args.text_cured
print_lines = args.diff
print_sort = args.sort

compare(text_ori, text_cured)
