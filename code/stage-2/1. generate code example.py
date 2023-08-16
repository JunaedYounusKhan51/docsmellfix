#!pip install openai
import os
import openai
import pandas as pd
import numpy as np
import time
import random

import backoff  # for exponential backoff


new_cycle_int = 1
new_cycle_number = "Cycle-"+str(new_cycle_int)

openai.organization = "xxx-XXXXXXXXXXXXXXXXXXXXXXXXXX"
openai.api_key = "xx-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"



@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


lazy_doc_df = pd.read_excel("lazy_doc_additional_description.xlsx")




generated_code_list = []


for idx,row in lazy_doc_df.iterrows():
	print(idx)

	code = row['Method Code']
	class_name = row['Class Name']
	documentation_new_gpt3 = row['New Documentation']
	method_name = row['Method Name']


	prompt = "Method Code:\n"+code+"\nClass:\n"+class_name+"\nDocumentation:\n"+documentation_new_gpt3+"\nGenerate a full executable and documented code example for the method "+method_name+" of class "+class_name+" based on the documentation:\n"
	zero_shot_results = dict()
	#response = openai.ChatCompletion.create(
	
	response = completions_with_backoff(
	    engine="text-davinci-002",
	    prompt=prompt,
	    temperature=0.2,
	    max_tokens=256,
	    top_p=1,
	    frequency_penalty=0,
	    presence_penalty=0,
	    best_of = 1,
	    #stop=["Code:"]
	)

	generated_code_list.append(response["choices"][0].text)

lazy_doc_df['Code Example ('+new_cycle_number+')'] = generated_code_list


lazy_doc_df.to_excel("lazy_doc_cycle"+str(new_cycle_int)+"_gen.xlsx", index=False)