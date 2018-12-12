import argparse
debug = False

# restores vowel by maximum liklihood using Viterbi algorithm
def restore_vowel(text, vocab_dict, lm_dict):
    with open(text) as f:
        content = f.readlines()
        for s in content:
            words = s.split()
            # manually add </s> to determine the the most likelihood
            words.append("</s>")
            # init from beginning of sentence
            prev_states = [("<s>", 0, "")]
            for w in words:
                curr_states = vocab_dict[w]
                temp_states = []
                for cur in curr_states:
                    max_state = (-999, "")
                    for (prev, alpha, sen) in prev_states:
                        prob = 0;
                        # read probability of bigram, back off to unigram if not found
                        if (prev, cur) in lm_dict[1]:
                            (logprob, backprob) = lm_dict[1][(prev, cur)]
                            prob = logprob
                        # back-off to unigram
                        else:
                            (logprob, backprob) = lm_dict[0][(cur,)]
                            (logprob_p, backprob_p) = lm_dict[0][(prev,)]
                            prob = logprob + backprob_p
                        # incorporate past states
                        prob = prob + alpha 
                        # store the max state as current state
                        if prob > max_state[0]:
                            max_state = (prob, sen + " " + cur)
                    # calculate current states to incorporate past states
                    temp_states.append((cur, max_state[0], max_state[1]))
                # store current states as previous states
                prev_states = temp_states
                if debug:
                    print w
                    for prev in prev_states:
                        print "     " + str(prev)
                    print
            print prev_states[0][2][1:-4]

# build a dict of <ngram, (logprob, backprob)> for each ngram
def build_lm(lm):
    with open(lm) as f:
        content = f.readlines()
        start = False
        ngrams_dicts = []
        n = 0
        for l in content:
            if not start and "\\1-grams:" in l:
                start = True
            if start and "\\" + str(n+1) + "-grams:" in l:
                ngrams_dicts.append({})
                n += 1
            elif start and "\\" not in l and l.strip():
                items = l.split()
                logprob = float(items[0])
                ngram = tuple(items[1:n+1])
                backprob = 0.0
                if len(items) > n+1:
                    backprob = float(items[n+1])
                ngrams_dicts[n-1][ngram] = (logprob, backprob)
        return ngrams_dicts

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
        # add </s> to ignore edge cases
        vocab_dict["</s>"] = ["</s>"]
        return vocab_dict
        
parser = argparse.ArgumentParser()
parser.add_argument("text")
parser.add_argument("vocab")
parser.add_argument("lm")
parser.add_argument("--debug", "-d", action='store_true')

args = parser.parse_args()
text = args.text
vocab = args.vocab
lm = args.lm
debug = args.debug

# build a (unvowelized word, vowelized options) dict for all vocab
vocab_dict = build_vocab(vocab)

# build a (ngram, (logprob, backprob)) dict for each ngram by reading lm
ngrams_dicts = build_lm(lm)

# restore unvowelized text 
restore_vowel(text, vocab_dict, ngrams_dicts)
