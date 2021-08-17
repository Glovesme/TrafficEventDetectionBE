import os
import random
import logging, json

import torch
import numpy as np
from seqeval.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import f1_score as f1

from transformers import BertConfig,AutoConfig, RobertaConfig
from transformers import BertTokenizerFast, AutoTokenizer, RobertaTokenizerFast

from model import JointEnhancedBERT, JointEnhancedRobBERT

MODEL_CLASSES = {
    'bertje': (BertConfig, JointEnhancedBERT, BertTokenizerFast),
    'robbert': (RobertaConfig, JointEnhancedRobBERT, RobertaTokenizerFast),
    'mbert': (BertConfig, JointEnhancedBERT, BertTokenizerFast),
    'xlm': (RobertaConfig, JointEnhancedRobBERT, RobertaTokenizerFast)
}

MODEL_PATH_MAP = {
    'bertje': 'GroNLP/bert-base-dutch-cased',
    'mbert': 'bert-base-multilingual-cased',
    'xlm': 'xlm-roberta-base',
    'robbert': 'pdelobelle/robbert-v2-dutch-base',
}


def get_intent_labels(args):
    return [label.strip() for label in open(os.path.join(args.data_dir, args.task, args.intent_label_file), 'r', encoding='utf-8')]


def get_slot_labels(args):
    return [label.strip() for label in open(os.path.join(args.data_dir, args.task, args.slot_label_file), 'r', encoding='utf-8')]


def load_tokenizer(args):
    return MODEL_CLASSES[args.model_type][2].from_pretrained(args.model_name_or_path)


def init_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)


def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if not args.no_cuda and torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)


def compute_metrics(intent_preds, intent_labels, slot_preds, slot_labels):
    assert len(intent_preds) == len(intent_labels) == len(slot_preds) == len(slot_labels)
    results = {}
    intent_result = get_intent_acc(intent_preds, intent_labels)
    slot_result = get_slot_metrics(slot_preds, slot_labels)
    sementic_result = get_sentence_frame_acc(intent_preds, intent_labels, slot_preds, slot_labels)

    results.update(intent_result)
    results.update(slot_result)
    results.update(sementic_result)

    return results


def compute_metrics_cls(intent_preds, intent_labels):
    assert len(intent_preds) == len(intent_labels)
    results = {}
    intent_result = get_intent_acc(intent_preds, intent_labels)
    results.update(intent_result)
    return results


def compute_metrics_ner(slot_preds, slot_labels):
    assert len(slot_preds) == len(slot_labels)
    results = {}
    slot_result = get_slot_metrics(slot_preds, slot_labels)
    results.update(slot_result)

    return results

def save_results(results, args):
    with open(args.result_dir, 'a') as outfile:
        results['train_batch_size'] = args.train_batch_size
        results['epochs'] = args.num_train_epochs
        results['model'] = args.model_type
        results['region'] = 'BRU' if args.task == 'traffic' else 'BE'
        json.dump(results, outfile)
        outfile.write('\n')


def get_slot_metrics(preds, labels):
    assert len(preds) == len(labels)
    return {
        "slot_precision": precision_score(labels, preds),
        "slot_recall": recall_score(labels, preds),
        "slot_f1": f1_score(labels, preds)
    }




def get_intent_acc(preds, labels):
    acc = (preds == labels).mean()
    # print(labels, '\n')
    # print(preds)
    intent_f1 = f1(labels, preds)

    return {
        "intent_acc": acc,
        "intent_f1": intent_f1,
    }


def read_prediction_text(args):
    return [text.strip() for text in open(os.path.join(args.pred_dir, args.pred_input_file), 'r', encoding='utf-8')]


def get_sentence_frame_acc(intent_preds, intent_labels, slot_preds, slot_labels):
    """For the cases that intent and all the slots are correct (in one sentence)"""
    # Get the intent comparison result
    intent_result = (intent_preds == intent_labels)

    # Get the slot comparision result
    slot_result = []
    for preds, labels in zip(slot_preds, slot_labels):
        assert len(preds) == len(labels)
        one_sent_result = True
        for p, l in zip(preds, labels):
            if p != l:
                one_sent_result = False
                break
        slot_result.append(one_sent_result)
    slot_result = np.array(slot_result)

    sementic_acc = np.multiply(intent_result, slot_result).mean()
    return {
        "sementic_frame_acc": sementic_acc
    }
