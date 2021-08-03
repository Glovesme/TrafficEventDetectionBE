import json


def read_file(input_file):
    """Reads a tab separated value file."""
    with open(input_file, "r", encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        return lines


def read_json_line(path):
    output = []
    with open(path, 'r') as f:
        for line in f:
            output.append(json.loads(line))

    return output


def write_json_line(data, path):
    with open(path, 'w') as f:
        for i in data:
            f.write("%s\n" % json.dumps(i))
    return None


def text_to_token_char_lists(text):
    tokens = text.split()
    # remove ''
    # for i in range(len(tokens) - 1, -1, -1):
    #     if tokens[i] != '':
    #         tokens = tokens[:i + 1]
    #         break

    token_char_list = list()
    char_idxs = list()
    for char_idx, character in enumerate(text):
        if char_idx == len(text) - 1:
            if len(char_idxs) != 0:
                token_char_list.append(char_idxs)
            if text[char_idx - 1] == ' ' and character != ' ':
                token_char_list.append([char_idx])

        elif character == ' ':
            if len(char_idxs) != 0:
                token_char_list.append(char_idxs)
            char_idxs = list()

        else:
            char_idxs.append(char_idx)

    assert len(tokens) == len(token_char_list)
    return token_char_list, tokens


def BIO_label(slot_dict, token_char_list, token_list):
    '''
    label dataset with BIO scheme
    :param slot_dict: dict contains different slot types
    :param token_char_list: a list in the form of [[token1_character1_offset, token1_character2_offset, ...], ]
    :param token_list: [token1_idx, token2_idx, ...]
    :return:
    '''
    bio_list = ['O' for i in range(len(token_list))]
    # slot_type = list(slot_dict.keys())[0]
    for slot_type in list(slot_dict.keys()):
        if slot_dict[slot_type] != 'Not Specified':
            for chunk in slot_dict[slot_type]:
                chunk_txt = chunk['chunk_txt']
                chunk_tok = chunk_txt.strip().split()
                chunk_tok_num = len(chunk_tok)
                chunk_offset = chunk['chunk_offset']
                for tok_idx, tok_char in enumerate(token_char_list):
                    if chunk_offset[0] in tok_char:
                        # calc token idx
                        for bio_idx in range(tok_idx, tok_idx + chunk_tok_num):
                            if bio_idx == tok_idx:
                                bio_list[bio_idx] = 'B-' + slot_type
                            else:
                                bio_list[bio_idx] = 'I-' + slot_type
                        # for bio_idx in range(tok_idx, tok_idx + chunk_tok_num):
                        #     try:
                        #         if bio_idx == tok_idx:
                        #             bio_list[bio_idx] = 'B-' + slot_type
                        #         else:
                        #             bio_list[bio_idx] = 'I-' + slot_type
                        #     except:
                        #         break
                        break
    return bio_list


def BIO_label2(slot_dict, token_char_list, token_list):
    '''
    label dataset with BIO scheme
    :param slot_dict: dict contains different slot types
    :param token_char_list: a list in the form of [[token1_character1_offset, token1_character2_offset, ...], ]
    :param token_list: [token1_idx, token2_idx, ...]
    :return:
    '''
    bio_list = ['O' for i in range(len(token_list))]
    # slot_type = list(slot_dict.keys())[0]
    for slot_type in list(slot_dict.keys()):
        if slot_dict[slot_type] != 'Not Specified':
            for chunk in slot_dict[slot_type]:
                chunk_txt = chunk['chunk_txt']
                chunk_tok = chunk_txt.strip().split()
                chunk_tok_num = len(chunk_tok)
                chunk_offset = chunk['chunk_offset']
                for tok_idx, tok_char in enumerate(token_char_list):
                    if chunk_offset[0] in tok_char:
                        # calc token idx
                        # for bio_idx in range(tok_idx, tok_idx + chunk_tok_num):
                        #     if bio_idx == tok_idx:
                        #         bio_list[bio_idx] = 'B-' + slot_type
                        #     else:
                        #         bio_list[bio_idx] = 'I-' + slot_type
                        for bio_idx in range(tok_idx, tok_idx + chunk_tok_num):
                            try:
                                if bio_idx == tok_idx:
                                    bio_list[bio_idx] = 'B-' + slot_type
                                else:
                                    bio_list[bio_idx] = 'I-' + slot_type
                            except:
                                break
                        # break
    return bio_list

if __name__ == '__main__':
    # txt = 'Eergisteren had ik een nachtmerrie over een gijzelingsactie op het werk . We zaten verschanst in de chauffagekamer . Goede schuilplaats .'
    # # a = {"where": [{"chunk_txt": "R20 Tegenwijzerzin ter hoogte van Rogiertunnel", "chunk_offset": [1, 46]}]}
    # b, c = text_to_token_char_lists(txt)
    # # e = BIO_label(a, b, c)
    a = read_file('data/intent.txt')
    b = read_file('data/label.txt')
    c = read_file('data/text.txt')
    for i, x in enumerate(zip(a,b,c)):
        print(x)
    print('done')

