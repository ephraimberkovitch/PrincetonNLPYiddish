# Project Language ~ 

This repository is the central point for documentation and data for your project. You will find several folders where you can store the data and code used as you create data and train models for a new language. 

`0_original_texts`: This folder contains the original text files for the project. This is a record of the original state of the texts before any pre-processing and annotation.

`1_lookups_data`: This folder contains the json lookups files for unambiguous lemmata, pos and ents. This data is used to document the bulk annotation process and is superseded by the manually annotated data from INCEpTION.

`2_new_language_object`: This folder contains the serialized nlp object from either Cadet or the Cadet notebook. This folder is fetched during training to load the new language object. It also contains the project.yml file. 

`3_inception_export`: This folder contains the CoNLL-U data that is exported from INCEpTION once annotation work is completed. If versioning of exports is required, you can place each version is its own subfolder. During training, this folder provides the main source of training data and should be split between training and validation sets.

`4_trained_models`: This folder contains packaged models and model cards for your new language models.
## Dataset Summary

Description of your language and your research goals.

## Languages

## Curation Rationale

## Source Data
- Provenance, how obtained
- Copyright

## Personal and Sensitive Information, Potential for Human Harm 

## Licensing Information


## Dataset Curators


## Citation Information

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

### Useful links
1. https://www.wikiwand.com/yi/%D7%9C%D7%99%D7%A1%D7%98%D7%A2_%D7%A4%D7%95%D7%9F_%D7%9C%D7%A9%D7%95%D7%9F-%D7%A7%D7%95%D7%93%D7%A9_%D7%95%D7%95%D7%A2%D7%A8%D7%98%D7%A2%D7%A8_%D7%90%D7%99%D7%9F_%D7%99%D7%99%D7%93%D7%99%D7%A9
2. 