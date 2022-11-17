
'''
pip install pyspellchecker
pip install langdetect
pip install googletrans==3.1.0a0
pip install transformers '''

from spellchecker import SpellChecker
from langdetect import detect
from googletrans import Translator
from transformers import (
        TokenClassificationPipeline,
        AutoModelForTokenClassification,
        AutoTokenizer,
    )
from transformers.pipelines import AggregationStrategy
import numpy as np
# Define keyphrase extraction pipeline
class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, model_outputs):
        results = super().postprocess(
            model_outputs=model_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])

def prepare_request(input):

    lan=detect(input)
    spell = SpellChecker(lan)

    x=input.split(" ")

    # find those words that may be misspelled
    misspelled = spell.unknown(x)

    for word in misspelled:
        # Get the one `most likely` answer
        print(spell.correction(word))

        # Get a list of `likely` options
        print(spell.candidates(word))
        
    for word in misspelled : 
        for y in range(len(x)) : 
            if x[y]==word : 
             x[y]=spell.correction(x[y])
    output=" ".join(x)

    translator = Translator()
    output_trans=translator.translate(output)
    request=output_trans.text


    # Load pipeline
    model_name = "ml6team/keyphrase-extraction-kbir-inspec"
    extractor = KeyphraseExtractionPipeline(model=model_name)

    print(request)

    u=extractor(request)

    return output , request , u

o , r , k = prepare_request("je cherech le pln du portée du management")
print("Output : "+o)
print("-----------------")
print("Resuest : "+r)
print("-----------------")
print(k)