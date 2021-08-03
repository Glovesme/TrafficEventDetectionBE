import random, os
import pandas as pd
from nltk.tokenize import TweetTokenizer
from utils import read_json_line, write_json_line, text_to_token_char_lists, BIO_label, read_file

tknzr = TweetTokenizer()
random.seed(123) # default 123


def preprocessing(tweet_text):
    '''
    Preprocess tweet text, including tokenize tweet and remove url
    :param tweet_text: string - original tweets
    :return: list of strings - tokenized tweet without url
    '''
    tokenized_tweet_text = tknzr.tokenize(tweet_text)
    processed_tweet = ' '.join(["" if word.startswith("http") or word == '\n' else word for word in tokenized_tweet_text])
    return processed_tweet


def label_data(json_data, file_dir):
    # def label_data(json_data, text_file_dir, label_file_dir, class_dir):
    '''
    label tweets
    :param file_dir: the dir for the labeled data
    :param json_data: .jonsl file contains the original tweets with annotations
    :return:
    '''

    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

    text_file_dir = file_dir + 'text.txt'
    label_file_dir = file_dir + 'label.txt'
    class_dir = file_dir + 'intent.txt'

    with open(text_file_dir, 'w', encoding='utf-8') as text_file, open(label_file_dir, 'w',
                                                                       encoding='utf-8') as label_file, open(class_dir, 'w', encoding='utf-8') as class_file:
        for data in json_data:
            slot_dict = {'what': data['what'], 'where': data['where'], 'when': data['when'],
                         'consequence': data['consequence']}

            # preprocess the tweet text
            preprocessed_tweet = preprocessing(data['text'])

            # map token to token characters
            token_char_list, token_list = text_to_token_char_lists(preprocessed_tweet)

            # tag tweet text with BIO schema
            bio_list = BIO_label(slot_dict, token_char_list, token_list)

            # remove # in the tokens
            text = preprocessed_tweet.split()
            new_text = []
            for token in text:
                if len(token) > 1 and token.startswith('#'):
                    new_text.append(token[1:])
                else:
                    new_text.append(token)

            # create tweet text file
            new_text = ' '.join(new_text)
            text_file.write(new_text + '\n')

            # create BIO label file
            bio_labels = ' '.join(bio_list)
            label_file.write(bio_labels + '\n')

            # create class label file
            if data['label'] == 1:
                label = 'traffic_related'
            else:
                label = 'non_traffic_related'
            class_file.write(label + '\n')


def creat_data_files(data_list, file_dir):
    '''
    create folders containing the data
    :param data_list: list of data
    '''
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_dir + '/seq.in', 'w', encoding='utf-8') as in_file, open(file_dir + '/seq.out', 'w', encoding='utf-8') as out_file, open(file_dir + '/label', 'w', encoding='utf-8') as label_file:
        for (text, intent, slot) in data_list:
            in_file.write(text+'\n')
            out_file.write(slot+'\n')
            label_file.write(intent + '\n')


def train_dev_test_split(input_text_dir, intent_label_dir, slot_label_dir,  out_dir, spllit_ratio=[0.6, 0.2, 0.2]):
    '''
    split data to train, dev, test sets, default ratio 0.6/0.2/0.2
    :param input_text_dir: the dir of the tweet text
    :param intent_label_dir: the dir of the class labels
    :param slot_label_dir: the dir of slot labels (BIO)
    :param out_dir: the dir for the results
    :param spllit_ratio: list - default ratio 0.6/0.2/0.2
    :return:
    '''
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    texts = read_file(input_text_dir)
    intents = read_file(intent_label_dir)
    slots = read_file(slot_label_dir)
    traffic_list = list()
    non_traffic_list = list()
    for i, (text, intent, slot) in enumerate(zip(texts, intents, slots)):
        if intent == 'traffic_related':
            traffic_list.append((text, intent, slot))
        else:
            non_traffic_list.append((text, intent, slot))
    traffic_len = len(traffic_list)
    non_traffic_len = len(non_traffic_list)

    # shuffle data
    random.shuffle(traffic_list)
    random.shuffle(non_traffic_list)
    train_data = traffic_list[:int(traffic_len*spllit_ratio[0])] + non_traffic_list[:int(non_traffic_len*spllit_ratio[0])]
    dev_data = traffic_list[int(traffic_len*spllit_ratio[0]): int(traffic_len*(spllit_ratio[0]+spllit_ratio[1]))] + non_traffic_list[int(non_traffic_len*spllit_ratio[0]):int(non_traffic_len*(spllit_ratio[0]+spllit_ratio[1]))]
    test_data = traffic_list[int(traffic_len*(spllit_ratio[0]+spllit_ratio[1])):] + non_traffic_list[int(non_traffic_len*(spllit_ratio[0]+spllit_ratio[1])):]

    # create files
    creat_data_files(train_data, out_dir+'/train')
    creat_data_files(dev_data, out_dir+'/dev')
    creat_data_files(test_data, out_dir+'/test')
    # return train_data, dev_data, test_data


if __name__ == '__main__':

    # Belgium data
    json_data = read_json_line('belgium_tweets_with_annotation.jsonl')
    label_data(json_data, 'be/')
    train_dev_test_split('be/text.txt', 'be/intent.txt', 'be/label.txt', 'be_traffic')

    # Bru data
    bru_json_data = read_json_line('bru_annotated_data_new.jsonl')
    label_data(bru_json_data, 'bru/')
    train_dev_test_split('bru/text.txt', 'bru/intent.txt', 'bru/label.txt', 'bru_traffic')

