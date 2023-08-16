#!pip install openai
import os
import openai
import pandas as pd
import numpy as np
import time
import random

import backoff  # for exponential backoff
import math
import re


new_cycle_int = 2
new_cycle_number = "Cycle-"+str(new_cycle_int)

prev_cycle_int = new_cycle_int-1
prev_cycle_number = "Cycle-"+str(prev_cycle_int) 



pre_prev_cycle_int = new_cycle_int-2
pre_prev_cycle_number = "Cycle-"+str(pre_prev_cycle_int)


openai.organization = "xxx-XXXXXXXXXXXXXXXXXXXXXXXXXXX"
openai.api_key = "xx-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"



@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


lazy_doc_df = pd.read_excel("lazy_doc_cycle"+str(prev_cycle_int)+"_eval.xlsx")




improve_possibility_list = []


def split_error_log(error_log):
	primary_split_error_list = error_log.split("\n")
	final_split_error_list = []
	for log in primary_split_error_list:
		if log != '\n' and log != "":
			log = log.strip()
			final_split_error_list.append(log)
	return final_split_error_list


def are_code_similar(code1, code2):
	code1 = re.sub(r"[\n\t\s]*", "", code1)
	code2 = re.sub(r"[\n\t\s]*", "", code2)
	if code1 == code2:
		return True
	return False


for idx, row in lazy_doc_df.iterrows():
	prev_output_msg = row['Output '+prev_cycle_number]
	pre_prev_output_msg = row['Output '+pre_prev_cycle_number]

	prev_code_example = row['Code Example ('+prev_cycle_number+')']
	pre_prev_code_example = row['Code Example ('+pre_prev_cycle_number+')']

	if are_code_similar(prev_code_example,pre_prev_code_example):
		try:
			if 'error' in pre_prev_output_msg.lower():
				improve_possibility_list.append('Not Possible in '+prev_cycle_number)
			else:
				improve_possibility_list.append('Already Passed')
		except:
			improve_possibility_list.append('Already Passed')
	else:
		improve_possibility_list.append("Possible")


lazy_doc_df['Improvement Possibility ('+prev_cycle_number+')'] = improve_possibility_list



new_output_msg_list = []

this_cycle_status_list = []





next_cycle_code_example_list = []


for idx, row in lazy_doc_df.iterrows():
	print(idx)
	output_msg = row['Output '+prev_cycle_number]
	this_cycle_code = row['Code Example ('+prev_cycle_number+')']
	improve_possibility = row['Improvement Possibility ('+prev_cycle_number+')']

	if "Not Possible" in improve_possibility:
		this_cycle_status_list.append("FAILED in " + prev_cycle_number)
		next_cycle_code_example_list.append(this_cycle_code)
		continue

	try:
		if 'error' in output_msg.lower():
			this_cycle_status_list.append("FAILED in " + prev_cycle_number)
			prompt = "Code with error:\n"+this_cycle_code+"\nError log:\n"+output_msg+"\nCorrect and rewrite the full code with proper package import based on the error log:\n"
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
			next_cycle_code_example_list.append(response["choices"][0].text)
		else:
			this_cycle_status_list.append("PASSED in " + prev_cycle_number)
			next_cycle_code_example_list.append(this_cycle_code)
	except:
		this_cycle_status_list.append("PASSED in " + prev_cycle_number)
		next_cycle_code_example_list.append(this_cycle_code)






lazy_doc_df[prev_cycle_number+" Status"] = this_cycle_status_list
lazy_doc_df['Code Example ('+new_cycle_number+')'] = next_cycle_code_example_list

lazy_doc_df.to_excel("lazy_doc_cycle"+str(new_cycle_int)+"_gen.xlsx", index=False)