import os
import sys
import logging
import csv
import math
import pandas


def to_tuples_array(file):
    text = file.readlines()
    array = []
    sentence = []
    tuple = ()
    ctr = 0

    for line in text:
        data = line.split("\t")
        if data[0] != "?" and len(line.strip()) > 0:
            word = data[0]
            pos = data[len(data)-1]
            pos = get_coarsetag(pos, 1)
            tuple = (word, pos.strip())
            sentence.append(tuple)
        elif data[0] == '?':
            array.append(sentence)
            sentence = []
            tuple = ()

            ctr += 1

            # print ctr

    # for i in range(0, len(array)):
    #   print array[i]

    return array


def get_coarsetag(tag, level):

    if level == 1:
        tag = tag.split("-")[0]
    elif level == 2:
        temp = tag.split("-")[1]
        tag = temp[:2]
    elif level == 3:
        temp = tag.split("-")[1]
        tag = temp[2:]

    return tag


def get_raw_data(file, column_no):
    """
    Get the labelled sentence from the csv file then convert
    it to array
    """

    FORMAT = "Reading: %(message)s"
    logging.basicConfig(format=FORMAT)

    r = csv.reader(file)

    if column_no == 0:
        text = []
        for row in r:
            if row[0] != "Questions":
                logging.info(row)
                text.append(row[0].strip())

        return text
    elif column_no == 1:
        category = []
        for row in r:
            if row[1] != "Category":
                logging.info(row)
                category.append(row[1])

        return category


def prune(tuple_array, sentences):
    """
    Extract the independent clause in the sentence.
    """

    conj = {"sapagkat", "dahil", "dahil sa", "at saka", "at hindi", "ni hindi",
            "pero", "datapwat", "ngunit", "subalit", "o", "o kaya",
            "gayon pa man", "gayumpaman", "gayunman", "kaya", "kung kaya't",
            "kung kaya", "man", "maging", "hindi lamang", "kundi", "bagaman",
            "bagama't", "kapag", "kasi", "dahilan sa", "gawa ng", "porke",
            "porke at", "porke't", "pagkat", "kaya", "kaysa", "kahit",
            "gayong", "kung", "kung gayon", "habang", "nang", "nang sa gayon",
            "maging", "maliban kung", "palibhasa", "para", "upang", "parang",
            "pansamantala", "hanggang"
            }

    q_words = {'aling', 'alin-alin', 'alin-aling', 'saang', 'saan-saan',
               'nasaan', 'nasaang', 'anong', 'anu-ano', 'anu-anong', 'inaano',
               'paanong', 'papaano', 'papaanong', 'sinong', 'sinu-sino',
               'sino-sinong', 'kailang', 'alin', 'saan', 'ano', 'kailan',
               'paano', 'sino', 'bakit'
               }

    for i in range(0, len(sentences)):
        temp = sentences[i].replace('?', '')
        text = temp.split(" ")

        for word in text:
            if word.lower() in conj:
                ind = text.index(word)

                # conjuction should not be too near in the beginning of the
                # sentence
                if len(text) >= 5 and ind >= math.ceil(len(text)/2):
                    tuple_array[i] = tuple_array[i][:ind]
                elif ind == 0:
                    for j in range(ind, len(text)):
                        if text[j].lower() in q_words:
                            tuple_array[i] = tuple_array[i][j:len(text)]
                            break

    # Scan each tuple array for arrays not starting with a wh-word
    for i in range(0, len(tuple_array)):
        if tuple_array[i][0][0] not in q_words:
            t = sentences[i].split(" ")

            for j in range(0, len(tuple_array[i])):
                if t[j].lower() in q_words:
                    tuple_array[i] = tuple_array[i][j:]

    # for i in range(0, len(tuple_array)):
    #   if tuple_array[i][0][0].lower() not in q_words:
    #       print tuple_array[i], sentences[i]

    return tuple_array


def get_sampling_data(sentence_list, category, dataset):
    """
    Return the set of data specfied. The sentences in the sentences list is assumed to contain only thet
    independents clause.

    sentence_list -- a list that contains sentences which is represented as an array of tuples (word and pos).
    category -- the label of the sentence
    dataset -- the type of data needed i.e training, testing or all
                1 - training set, 2 - testing set, 3 - all
    """

    FORMAT = "Getting: %(message)s"
    logging.basicConfig(format=FORMAT)

    array = []

    # get the training data which is the 80% of the dataset
    if dataset == 1:
        y = int(math.ceil(len(sentence_list)*0.8))

        for i in range(0, y):
            data = []

            for j in range(0, len(sentence_list[i])):
                if j == 0:
                    data.append(sentence_list[i][j][0].lower())
                else:
                    data.append(sentence_list[i][j][1].lower())

            data.append(category[i].lower())
            logging.info(data)
            array.append(data)
    # get the testing data which is the remaining 20% of the dataset
    elif dataset == 2:
        x = int(len(sentence_list) - math.ceil(len(sentence_list)*0.2))

        for i in range(x, len(sentence_list)):
            data = []

            for j in range(0, len(sentence_list[i])):
                if j == 0:
                    data.append(sentence_list[i][j][0].lower())
                else:
                    data.append(sentence_list[i][j][1].lower())

            data.append(category[i].lower())
            logging.info(data)
            array.append(data)
    # get all the data in the dataset
    elif dataset == 3:
        for i in range(0, len(sentence_list)):
            data = []

            for j in range(0, len(sentence_list[i])):
                if j == 0:
                    data.append(sentence_list[i][j][0].lower())
                else:
                    data.append(sentence_list[i][j][1].lower())

            data.append(category[i].lower())
            logging.info(data)
            array.append(data)

    return array


def write_to_file(**kwargs):
    path = os.path.abspath('../files/transformed_data.csv')

    field_names = kwargs.keys()
    data_frame = pandas.DataFrame()

    for field in field_names:
        value = kwargs.get(field)
        string_array = []

        for v in value:
            s = ','.join(v)
            string_array.append(s)

        data_frame = pandas.concat([data_frame, pandas.DataFrame(
            data=string_array, columns=[field])], axis=1)

    data_frame.to_csv(path, index=False)


def format(args):
    input1 = open(os.path.abspath('files/pos_tagger.out'))
    input2 = open(os.path.abspath('files/raw_data/labelled_data.csv'))
    input3 = open(os.path.abspath('files/raw_data/labelled_data.csv'))

    word_and_pos = to_tuples_array(input1)
    sentence = get_raw_data(input2, 0)
    category = get_raw_data(input3, 1)

    input1.close()
    input2.close()
    input3.close()

    pruned_array = prune(word_and_pos, sentence)

    if args[1] == 'random':
        training = get_sampling_data(pruned_array, category, 1)
        testing = get_sampling_data(pruned_array, category, 2)

        return training, testing

    elif args[1] == 'stratified':
        category_list = ['abbreviation', 'description', 'entity', 'human', 'location', 'numeric']
        training = []
        testing = []
        start = 0

        for label in category_list:
            # get all sentence with the same label
            for index in range(start, len(category)):
                if category[index] != label:
                    strata_sentence_list = pruned_array[start:index-1]
                    strata_category = category[start:index-1]
                    strata_training_set = get_sampling_data(strata_sentence_list, strata_category, 1)
                    strata_testing_set = get_sampling_data(strata_sentence_list, strata_category, 2)
                    training.append(strata_training_set)
                    testing.append(strata_testing_set)
                    start = index
                    break
        print(training)

        return training, testing

    # print len(pruned_array)
    # print len(fpFormat)

    # write_to_file(fpFormat)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    format(sys.argv)
