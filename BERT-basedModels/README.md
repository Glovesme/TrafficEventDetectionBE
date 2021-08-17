This directory contains the code for BERT-based models used in our paper.
The code is based on Pytorch.

## Dependencies
pytorch==1.7.1

scikit-learn==0.24.1

transformers==4.2.2

## Usage

```bash

 
$ python3 main.py --task {task_name} \
                  --model_type {model_type} \
                  --model_dir {model_dir_name} \
                  --do_train --do_eval \
                  --jointmode {True or False} \
                  --mode {0 or 1} \
                  --result_dir {dir_of_results}

# Example: for BRU dataset using joint enhanced bertje
$ python3 main.py --task bru \
                  --model_type bertje \
                  --model_dir bru_Joint_bertje \
                  --do_train --do_eval \
                  --jointmode True \
                  --result_dir result/bru_Joint_bertje.jsonl
                  
# Example: text classification on BE dataset
$ python3 main.py --task be \
                  --model_type mbert \
                  --model_dir be_tc_mbert \
                  --do_train --do_eval \
                  --jointmode False \
                  --mode 0 \
                  --result_dir result/be_text_cls_mbert.jsonl
                  
# Example: slot filling on BE dataset
$ python3 main.py --task be \
                  --model_type mbert \
                  --model_dir be_sf_mbert \
                  --do_train --do_eval \
                  --jointmode False \
                  --mode 1 \
                  --result_dir result/be_slot_filling_mbert.jsonl                  
```

## Data
### Format
Each dataset is a folder under the ```./data``` folder, where each sub-folder indicates a train/dev/test split:
```
./data
└── bru
    ├── test
    │   ├── label
    │   ├── seq.in
    │   └── seq.out
    ├── train
    │   ├── label
    │   ├── seq.in
    │   └── seq.out
    └── dev
        ├── label
        ├── seq.in
        └── seq.out
```
In each sub-folder,<br> 
* ```label``` file contains the text labels.<br> 
    e.g. ```Traffic-related```

* ```seq.in``` file contains tweets as the input sequences. Each line indicates one tweet and words are separated by a single space.<br>
    e.g. ```car accident on Etterbeek```

* ```seq.out``` file contains ground truth slot labels. Each line indicates a sequence of slot labels and the [BIO tagging scheme](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)) is used.<br>
    e.g. ```O B-what I-what O O B-where I-where O```
    
### Prepare the data

According to the [format](#format), you should prepare under the ```BERT-basedModels/data``` directory the two datasets with folder names ```bru``` and ```be```.

 
## Acknowledgment

https://github.com/monologg/JointBERT

https://github.com/czhang99/Capsule-NLU/blob/master/README.md#data

