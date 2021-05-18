# Project Language ~ 

This repository is the central point for documentation and data for your project. You will find several folders where you can store the data and code used as you create data and train models for a new language. 

`0_original_texts`: This folder contains the original text files for the project. This is a record of the original state of the texts before any pre-processing and annotation.

`1_lookups_data`: This folder contains the json lookups files for unambiguous lemmata, pos and ents. This data is used to document the bulk annotation process and is superseded by the manually annotated data from INCEpTION.

`2_corpus_json`: This folder contains the corpus.json file used to asses the number of tokens that should be automatically bulk annotated. It is used purely for documentation purposes.

`3_cadet_export`: This folder should contain the conllu_export.zip file that is created by either Cadet or the Cadet notebook. The files inside constitute the starting point for annotation work in INCEpTION and are superseded by the INCEpTION export files.

`4_new_language_object`: This folder contains the serialized nlp object from either Cadet or the Cadet notebook. This folder is fetched during training to load the new language object. It also contains the project.yml file. 

`5_inception_export`: This folder contains the CoNLL-U data that is exported from INCEpTION once annotation work is completed. If versioning of exports is required, you can place each version is its own subfolder. During training, this folder provides the main source of training data and should be split between training and validation sets.

`6_trained_models`: This folder contains packaged models and model cards for your new language models.
## Description

Description of your language and your research goals.


## Getting Started



### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10


## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)
