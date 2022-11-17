import json

from django.core.serializers import serialize
from itertools import permutations
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from owlready2 import *

onto_file = get_ontology("D:/--Etudes--/5DS/PROJET AI/New folder/Projet-IA-Cognition/finalontolgyV2.owl").load()


# functions from scratch
# functions ------------------------
from app.forms import ArticleForm

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
    if (lan == "en"):
        spell = SpellChecker(lan)

        x=input.split(" ")

        # find those words that may be misspelled
        misspelled = spell.unknown(x)
        """""
        for word in misspelled:
           
             print(spell.correction(word))
    
            # Get a list of `likely` options
            #print(spell.candidates(word))
         """
        for word in misspelled :
            for y in range(len(x)) :
                if x[y]==word :
                 x[y]=spell.correction(x[y])
        output=" ".join(x)

        translator = Translator()
        output_trans=translator.translate(output)
        request=output_trans.text
    else :
        translator = Translator()
        output_trans = translator.translate(input)
        request = output_trans.text


    # Load pipeline
    model_name = "ml6team/keyphrase-extraction-kbir-inspec"
    extractor = KeyphraseExtractionPipeline(model=model_name)

    #print(request)

    u=extractor(request)


    return u
"""""
o , r , k = prepare_request("i wnt to serch for the scope management plan and the projct charter")
print("Output : "+o)
print("-----------------")
print("Resuest : "+r)
print("-----------------")
print(k)
# functions ------------------------
"""""

# Create your views here.

def index(request):
    return render(request,"index.html")

def context_suggest(request):
    name=request.GET['name']
    token = name.split(" ")[-1]
    suf =""
    for p in range (len(name.split(" "))-1):
        suf= suf +" "+name.split(" ")[p]

    #name=name.replace(" ","_c ")
    name=token
    if(name==""):
        print("test")
    lperm=[]
    lperm=name.split("_")
    lperm=list(permutations(lperm, len(lperm)))

    dict=[]
    print(lperm)
    for i in lperm:
        word="*_"
        word=word.join(i)
        print(word)
        for j in range(len(list(onto_file.search(iri='*'+word+'**')))):
            dict.append(list(onto_file.search(iri='*' + word + '**'))[j])

    final = []
    print(dict)
    for i in dict:
        word = str(i)
        x = word.split(".")
        word = x[1]
        final.append(word)
    ff=[]
    for i in range(len(final)):
        ff.append({"id":i,"name":suf+" "+final[i].replace("_"," ")})
    json_obj=json.dumps(ff)
    return HttpResponse(json_obj)


def extract_data():
    import pandas as pd
    df = pd.read_csv('D:/--Etudes--/5DS/PROJET AI/New folder/df_final_presyn.csv')
    Concepts = df['Process_name'].unique()
    dict_result = {}
    dict_inputs = {}
    dict_outputs = {}
    dict_tat = {}
    for i in range(len(Concepts)):
        df0 = df[df['Process_name'] == Concepts[i]]
        df_inputs = df0[df0['Type'] == 'has_inputs']
        df_inputs.reset_index(inplace=True)

        df_outputs = df0[df0['Type'] == 'outputs']
        df_outputs.reset_index(inplace=True)
        df_tat = df0[df0['Type'] == 'has_techniques_and_tools']
        df_tat.reset_index(inplace=True)
        for j in range(len(df_inputs)):
            dict_inputs[df_inputs['Concept'][j]] = df_inputs['Definition'][j]
        for w in range(len(df_outputs)):
            dict_outputs[df_outputs['Concept'][w]] = df_outputs['Definition'][w]
        for z in range(len(df_tat)):
            dict_tat[df_tat['Concept'][z]] = df_tat['Definition'][z]
        test = Concepts[i].replace(' ', '_')
        dict_result[Concepts[i]] = {
            'inputs': dict_inputs,
            'outputs': dict_outputs,
            'tat': dict_tat,
            'Def': getattr(onto_file, test).isDefinedBy[0]
        }
    return dict_result

dict_result= extract_data()

def OWL_Concept(Concept):

    list=dict_result.keys()
    for i in list:
        if Concept in dict_result[i]['inputs'].keys():
            for j in dict_result[i]['inputs'].keys():
                if j == Concept:
                    return dict_result[i]['inputs'][Concept],'inputs',i,dict_result[i]['Def']
        if Concept in dict_result[i]['outputs'].keys():
            for j in dict_result[i]['outputs'].keys():
                if j == Concept:
                    return dict_result[i]['outputs'][Concept],'Outputs',i,dict_result[i]['Def']
        if Concept in dict_result[i]['tat'].keys():
            for j in dict_result[i]['tat'].keys():
                if j == Concept:
                    return dict_result[i]['tat'][Concept],'Techniques and Tools',i,dict_result[i]['Def']
    return "","","",""






def OWL(Process):
    return dict_result[Process]['inputs'],dict_result[Process]['outputs'],dict_result[Process]['tat'],dict_result[Process]['Def']

def context_result1(request):
    dict=[]
    name= request.POST.get('name')
    #rint(str(name)+ "^^^$$$$$$")
    wezza=prepare_request(name)
    print (str(wezza[0])+"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    for j in range(len(list(onto_file.classes()))):
        dict.append(list(onto_file.classes())[j])
    final = []
    print(dict)
    for i in dict:
        word = str(i)
        x = word.split(".")
        word = x[1]
        final.append(word)

    my_dict = {"Name":[],"Details":[]};
    for i in wezza:
        i= i.split(" ")
        for z in i :
            for classee in final:
                if (z in classee):
                    classee= classee.replace("_"," ")

                    if(classee in dict_result.keys()):
                        if OWL(classee)!= "":
                            a,b,c,d =OWL(classee)
                            my_dict["Name"].append(str(classee))
                            my_dict["Details"].append(d)


    my_dict["Name"] =[*set(my_dict["Name"])]
    my_dict["Details"] =[*set(my_dict["Details"])]

    my_list=zip(my_dict["Name"],my_dict["Details"])

    context={
       "my_list" : my_list
    }
    print (context)
    return render(request,"list_result.html",context)


def details (request):
    Name=request.GET["Name"]
    a, b, c, d = OWL(Name)
    my_dict = {"Name": Name, "Details": d, "Input": a, "Output": b, "tat": c};

    return render(request, "detail.html", my_dict)