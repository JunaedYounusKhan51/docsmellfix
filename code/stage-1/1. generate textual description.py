#!pip install openai
import os
import openai
import pandas as pd
import numpy as np
import time
import random


openai.organization = "xxx-XXXXXXXXXXXXXXXXXXXXXXX"
openai.api_key = "xx-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"



lazy_doc_df = pd.read_excel("lazy_doc_with_source_code.xlsx")


oneshot_df = pd.read_excel('non-smelly-documentation.xlsx')
example_code= random.choice(oneshot_df['Method Code'].tolist())
example_doc = random.choice(oneshot_df['Documentation Text'].tolist())


generated_doc_list = []


for idx,row in lazy_doc_df.iterrows():
	print(idx)
	code = row['Method Code']


	prompt = "Method Code:\n"+example_code+"\nDocumentation:\n"+example_doc+'\nMethod Code:\n'+code+"\n"+"Documentation:\n"
	one_shot_results = dict()
	response = openai.Completion.create(
	    engine="text-davinci-002",
	    prompt=prompt,
	    temperature=0.2,
	    max_tokens=256,
	    top_p=1,
	    frequency_penalty=0,
	    presence_penalty=0,
	    best_of = 1,
	    stop=["Code:"]
	)

	generated_doc_list.append(response["choices"][0].text)

lazy_doc_df['New Documentation'] = generated_doc_list


lazy_doc_df.to_excel("lazy_doc_additional_description.xlsx", index = False,encoding='utf8')