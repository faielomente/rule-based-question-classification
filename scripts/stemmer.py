import re
import csv
import os


infix = ['um', 'in']
prefix = [
    'makapang', 'nakapang', 'nakapan', 'makapan', 'nakapam',
    'makapam', 'nakapag', 'makapag', 'nagpati', 'magpati', 'nagpaka',
    'magpaka', 'magpapa', 'nagpapa', 'nagkaka', 'magkaka', 'ipakipa',
    'ikapang',  'naipag', 'mangag', 'nangag', 'kasing', 'ipang', 'pinag',
    'papag', 'mapag', 'kapag', 'napag', 'ipaki', 'magka', 'magsi',
    'nagka', 'magma', 'nagma', 'magpa',  'nagpa', 'maipa', 'naipa',
    'kasim', 'pagpa', 'paka', 'paki', 'pang', 'ipag', 'mang', 'nang',
    'maka', 'naka', 'mapa', 'napa', 'ika', 'pag', 'isa', 'ipa', 'mai',
    'nai', 'mag', 'nag', 'man', 'nan', 'mam', 'nam', 'ma', 'na', 'ka',
    'pa'
]
suffix = ['han', 'hin', 'an', 'in', 'ng']
vowel = ['a', 'e', 'i', 'o', 'u']


def strip_infix(word):
    dictionary = {'word': "", 'infix': "_"}

    for inf in infix:
        if (inf in word):
            start_pos = re.search(inf, word).start()
            end_pos = re.search(inf, word).end()

            # checks the position of infix; removes infix only if in the
            # middle,start position, or word length > 3
            if (start_pos >= 0 and end_pos < len(word) and len(word) > 4):
                # if word ! in dictionary
                word = re.sub(inf, '', word, 1)

            dictionary['infix'] = inf

    dictionary['word'] = word

    return dictionary

###


def strip_suffix(word):
    d = {'word': "", 'suffix': "_"}

    for suf in suffix:
        if (suf in word):
            if(word.endswith(suf) and len(word) > 4):
                word = re.sub(suf+'$', '', word, 1)
                d['suffix'] = suf

    d['word'] = word

    return d

###


def strip_prefix(word):
    # temp_word,prefix_found,the_prefix
    d = {'word': "", 'prefix': "_", 'has_pref': False}

    for pre in prefix:
        if(pre in word):
            if(word.startswith(pre) and len(word) > 5):
                word = re.sub(pre, '', word, 1)
                d['prefix'] = pre
                d['has_pref'] = True

        if word.startswith("-"):
            word = word[1:]

        # checks reduplication of vowel prefixes
        for char in vowel:
            if(word.startswith(char) and len(word) > 1):
                if(word[0] == word[1]):
                    word = word[1:]

        # word = check_reduplication(word)
        d['word'] = word

    return d

###


def check_reduplication(word):
    d = {'word': "", 'redup': "_"}

    for i in range(1, 3):
        if word[:i] == word[i:i+i]:  # python substring;
            word = word[i:]
            d['redup'] = word[:i]
            break

    d['word'] = word

    return d


def format_data(input, output):
    """
    Coverts the horizontal sentences into vertical sentences including the question mark.
    Each sentence is separated by a single space.
    Receives an input file with cleaned data.
    Outputs a file cointaning vertical sentences.
    """
    input_file = input
    output_file = output
    csv_f = csv.reader(input_file)
    ctr = 0

    for row in csv_f:
        # print row
        if ctr == 0:
            ctr += 1
        else:
            for column in range(0, len(row) - 1):
                sen = row[column].split(" ")
                for word in sen:
                    if '?' in word:
                        word = word.replace('?', '')
                        output_file.write(word)
                        output_file.write("\n")
                        output_file.write("?")
                        output_file.write("\n")
                        output_file.write("\n")
                    elif word != "":
                        output_file.write(word)
                        output_file.write("\n")

    input_file.close()
    output_file.close()


def write_to_file(stemmed_data):
    """
    Write into a file the output of stemming.
    """
    output_file = open(os.path.abspath('./files/stemmer.out'), 'w')

    for dict in stemmed_data:
        output_file.write(dict['word'])
        output_file.write(" ")
        output_file.write(dict['root'])
        output_file.write(" ")
        output_file.write(dict['prefix'])
        output_file.write(" ")
        output_file.write(dict['infix'])
        output_file.write(" ")
        output_file.write(dict['suffix'])
        output_file.write(" ")
        output_file.write(dict['redup'])
        output_file.write(" ")
        output_file.write("XXX")
        output_file.write("\n")

        if dict['word'] == "?":
            output_file.write("\n")

    output_file.close()


def count_qmark(file):
    """
    For debugging purposes
    Count and display the number of sentences in the raw data by counting the number of question mark.
    """
    text = file.readlines()
    ctr = 0

    for line in text:
        if "?" in line:
            ctr += 1

    print(ctr)
    file.close()


def main():
    input = open(os.path.abspath('./files/raw_data/labelled_data.csv'))
    output = open(os.path.abspath('./files/stemmer.out'), 'w+')

    # Rearrange the data into vertical sentences.
    # Each sentence ending with a questions mark.
    format_data(input, output)

    # Reads the output file of format_data().
    wordfile = open(os.path.abspath('./files/stemmer.out'))
    # for debugging
    # wordfile = open(os.path.abspath('preprocessing/test_stemmer.txt'))

    stemmed_data = list()

    # And each word in the file is stemmed.
    for w in wordfile.readlines():
        if len(w.strip()) > 0:
            infix_dict = {'word': "", 'infix': "_"}
            pref_dict = {'word': "", 'prefix': "_", 'has_pref': False}
            redup_dict = {'word': "", 'redup': "_"}
            suf_dict = {'word': "", 'suffix': "_"}
            morphology = {
                'word': "", 'root': "", 'prefix': "_", 'infix': "_",
                        'suffix': "_", 'redup': "_"
            }
            root = w
            temp_word = w
            if len(w) > 5:
                infix_dict = strip_infix(w.lower())  # remove any infix first
                temp_word = infix_dict['word']

            # usually root words are 4-5 characters in length
            if len(temp_word.strip()) >= 5:
                # try to check prefixes, suffixes and reduplications
                pref_dict = strip_prefix(temp_word)
                temp_word = pref_dict['word']
                suf_dict = strip_suffix(temp_word)
                temp_word = suf_dict['word']
                redup_dict = check_reduplication(temp_word)
                temp_word = redup_dict['word']

            root = temp_word

            morphology['word'] = w.strip()
            morphology['root'] = root.strip()
            morphology['prefix'] = pref_dict['prefix']
            morphology['infix'] = infix_dict['infix']
            morphology['suffix'] = suf_dict['suffix']
            morphology['redup'] = redup_dict['redup']

            # Append the stemmed words in the list of stemmed data.
            # print(w.strip(), root.strip())
            stemmed_data.append(morphology)

    # Write the stemmed data into a file as an output.
    write_to_file(stemmed_data)
    # print(stemmed_data)

    wordfile.close()


if __name__ == "__main__":
    main()
#     count_qmark(open(os.path.abspath('./files/stemmer.out')))
