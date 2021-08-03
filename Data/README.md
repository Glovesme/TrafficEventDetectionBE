# Traffic Twitter Datasets
This directory contains the instructions on how to download and use the datasets we created.

## Dataset files
- Three `.jsonl` files are provided which contain useful information about the datasets:
    - `bru_annotated_id_offsets.jsonl` is the Brussels dataset
    - `be_annotated_id_offsets.jsonl` is the Belgium dataset (include tweets from Brussels)
    - `be_annotated_id_offsets(except_bru).jsonl` is the Belgium dataset (exclude tweets from Brussels)

- Each `.jsonl` file has the following attributes:
    - `id`: the tweet ID which can be used to crawl the tweet from the Twitter server
    - `label`: the label of each tweet, `0` means the tweet is non-traffic-related, `1` means it is traffic-related
    - `what`: contains the chunk offset (character offset) which indicates **What  happened  during  the  reportedtraffic-related tweets?**
    - `where`: contains the chunk offset (character offset) which indicates **Where did the reportedtraffic-related  tweets  happen?**
    - `when`: contains the chunk offset (character offset) which indicates **When didthe reported traffic-related tweets happen**
    - `consequence`: contains the chunk offset (character offset) which indicates **What is the CONSE-QUENCE of the reported traffic event?**

- Note: The chunk offsets are obtained from the preprocessed tweets
