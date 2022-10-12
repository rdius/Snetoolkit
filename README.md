### Snetoolkit is a set of tools that helps to deal with Spatial Named Entities (SNE). There are three mains functionnalities:

* Extraction of SNE from textual document : this function is based on spacy
* SNE Geocoding : gives coordinate of a given SNE based on the Geonames DataBase. There two type of geocoding 
     * default candidate geocoding : return one candidate that corresponds to the default result of Geoname
     * multi candidates geocoding  : return a top@X (e.g, top@10 - frist 10 results) candidates from Geonames result
* Disambiguation of ambiguous SNE
   * this function is based on multiple technics, that helps to disambiguate ambiguous SNE. Based on the multi candidate geocoding, the disambiguation is supposed to return the right candidate from the multiple ones.

