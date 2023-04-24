######################################################
# Project: Project 3
# UIN: 676977984
# repl.it URL: https://replit.com/@CS111-Fall2021/Project-3-LilyEap1#main.py

# For this project, I received help from the following members of CS111.
# Ethan Gong, netID 659621197 : help with bar graph
 
######################################################
######################################################
######################################################
import csv
import json
import requests
import matplotlib.pyplot as plt

#functions that will be used for questions:
def get_data_from_file(fn, format=""):
  ''' receive file --> determine file type --> open file --> return file as a list'''
  a = fn[-4:]
  data = []
  if a == ".csv":
    f = open(fn)
    reader = csv.reader(f)
    for row in reader:
      data.append(row)
    f.close()
  elif a == "json":
    f = open(fn)
    data = json.load(f)
    f.close()
  return data

def get_data_from_internet(url):
  '''receive url --> return url as json '''
  link = url
  f = requests.get(link)
  data = f.json()
  return data

def get_state_name(state_names, state_code):
  '''receive dictionary and state code --> returns the name of the state'''
  for statesdict in state_names:
    if statesdict["abbreviation"] == state_code:
      name = statesdict["name"]
  return name

def get_state_population(state_populations, state_name):
  '''receive dictionary of state pop and state code --> returns population of that state'''
  state_name = "." + state_name
  state_name = state_name.upper()
  for statesdict in state_populations:
    for states in statesdict.keys():
      upperstate = states.upper()
      if state_name == upperstate:
        statepop = statesdict.get(states)
        return statepop

def get_index_for_column_label(header_row, column_label):
  '''receives a list & index number --> returns index position for that label'''
  index = header_row.index(column_label)
  return index

######################################################
  #storing data into variables 
######################################################

#getting the data and storing them into variables
taxdata = get_data_from_file("tax_return_data_2018.csv")
statetitle = get_data_from_file("states_titlecase.json")
popdata = get_data_from_internet("https://raw.githubusercontent.com/heymrhayes/class_files/main/state_populations_2018.txt")

#getting indices of certain categories and storing them into variables
firstrow = taxdata[0]
agiindex = get_index_for_column_label(firstrow, "agi_stub")
incomeindex = get_index_for_column_label(firstrow, "A04800")
taxreturnindex = get_index_for_column_label(firstrow, "N04800")
totalreturnindex = get_index_for_column_label(firstrow, "N1")
stateindex = get_index_for_column_label(firstrow, "STATE")
dependentsindex = get_index_for_column_label(firstrow, "NUMDEP")

######################################################
  #national level questions
######################################################
#What is the average taxable income per return (all returns, not just returns with taxable income) across all groups?
#A04800 / N1 by ALL
def avgtax_income_national():
  '''returns average taxable income per return across all groups'''
  totalincome = 0
  totalreturn = 0 
  for row in taxdata:
    if row != taxdata[0]:
      totalincome += int(row[int(incomeindex)])
      totalreturn += int(row[int(totalreturnindex)])
  avgtax = totalincome / totalreturn * 1000
  avgtax = int(round(avgtax))
  return avgtax

#What is the average taxable income per return (all returns, not just returns with taxable income) for each agi group?
#A04800 / N1 by AGI
def avgtax_income_per_group(agi):
  ''' average taxable income per return for each agi group'''
  groupincome = 0
  groupreturn = 0
  for row in taxdata:
    if row[agiindex] == agi:
      groupincome += int(row[int(incomeindex)])
      groupreturn += int(row[int(totalreturnindex)])
  avgtax = groupincome / groupreturn * 1000
  avgtax = int(round(avgtax))
  return avgtax

#What is the average taxable income (per resident) per state?
states_income_dict = {}
for i in range(1, len(taxdata)):
  row = taxdata[i]
  state_code = row[stateindex]
  if state_code in states_income_dict:
    states_income_dict[state_code]["taxable income"] += int(row[incomeindex])
  else:
    states_income_dict[state_code] = {"taxable income": int(row[incomeindex])}
    
for state_code in states_income_dict:
  state_name = get_state_name(statetitle, state_code)
  state_population = get_state_population(popdata, state_name)
  avgtax = round(states_income_dict[state_code]["taxable income"] / state_population * 1000)
  states_income_dict[state_code]["average"] = avgtax


######################################################
  #state level questions
######################################################
#what is the average taxable income per return across all groups?
#A04800 / N1 by STATE
def avgtax_income_per_return_state(state):
  '''receives state code --> returns average taxable income per return across all groups'''
  groupincome = 0
  groupreturn = 0    
  for row in taxdata:
    if row[stateindex] == state:
      groupincome += int(row[int(incomeindex)])
      groupreturn += int(row[int(totalreturnindex)])
  avgtax = groupincome / groupreturn * 1000
  avgtax = int(round(avgtax))
  return avgtax

#what is the average taxable income per return for each agi group?
#A04800 / N1 by STATE AND AGI
def avgtax_income_per_return_state_group(state, agi):
  '''receives state code & agi --> returns average taxable income per return for an agi group'''
  groupincome = 0
  groupreturn = 0 
  for row in taxdata:
    if row[stateindex] == state and row[agiindex] == agi:
      groupincome += int(row[int(incomeindex)])
      groupreturn += int(row[int(totalreturnindex)])
  avgtax = groupincome / groupreturn * 1000
  avgtax = int(round(avgtax))
  return avgtax

#what is the average dependents per return for each agi group?
#NUMDEP / N1 by STATE AND AGI
def avgtax_dependents_per_return_state_group(state, agi):
  '''receives state code & agi --> returns average dependents per return for an agi group'''
  dependents = 0
  groupreturn = 0 
  for row in taxdata:
    if row[stateindex] == state and row[agiindex] == agi:
      dependents += int(row[int(dependentsindex)])
      groupreturn += int(row[int(totalreturnindex)])
  avgdependents = dependents / groupreturn
  avgdependents = round(avgdependents, 2)
  return avgdependents

#what is the percent of returns with no taxable income per agi group?
#1 - (N04800 /  N1) by STATE AND AGI
def perc_of_returns_no_taxincome_state_group(state, agi):
  '''receives state code & agi --> returns percent of returns with no taxable income for an agi group'''
  taxable_inc = 0
  totalreturn = 0 
  for row in taxdata:
    if row[stateindex] == state and row[agiindex] == agi:
      taxable_inc += int(row[int(taxreturnindex)])
      totalreturn += int(row[int(totalreturnindex)])
  nontax_percent = (1 - (taxable_inc / totalreturn)) * 100
  return nontax_percent 

#what is the average taxable income per resident?
#A04800 / POPULATION by STATE
def avgtax_income_per_resident_state(state):
  '''receives state code --> returns average taxable income per resident'''
  groupincome = 0
  fullstatename = get_state_name(statetitle, state)
  statepop = get_state_population(popdata, fullstatename)
  for row in taxdata:
    if row[stateindex] == state:
      groupincome += int(row[int(incomeindex)])
  avgtax = groupincome / statepop * 1000
  avgtax = int(round(avgtax))
  return avgtax 

#what is the percentage of returns for each agi_group?  (as a percentage of total returns for that state)
# by STATE AND AGI
def perc_returns_state_group(state,agi):
  '''receives state code & agi --> returns percentage of returns for an agi_group'''
  totalreturn = 0
  agireturn = 0
  for row in taxdata:
    if row[stateindex] == state and row[agiindex] == agi:
      agireturn += int(row[int(totalreturnindex)])
    if row[stateindex] == state:
      totalreturn += int(row[int(totalreturnindex)])
  percent = agireturn / totalreturn * 100
  return percent

#what is the percentage of taxable income for each agi_group? (as a percentage of total taxable income for that state)
#N04800 /  N1 by STATE AND AGI
def perc_taxincome_state_group(state,agi):
  '''receives state code & agi --> returns percentage of taxable income for an agi_group'''
  group_taxincome = 0
  total_taxincome = 0 
  for row in taxdata:
    if row[stateindex] == state and row[agiindex] == agi:
      group_taxincome += int(row[int(incomeindex)])
    if row[stateindex] == state:
      total_taxincome += int(row[int(incomeindex)])
  tax_percent = group_taxincome / total_taxincome * 100
  return tax_percent

######################################################
  #answers.txt
######################################################
def answer_header(question_number, question_labels):
 ''' returns the header string for each answer'''
 header = "\n"*2
 header += "="*60 + "\n"
 header += "Question " + str(question_number) + "\n"
 header += question_labels[question_number] + "\n"
 header += "="*60 + "\n"
 return header
 
 
question_labels = [
   "",
   "average taxable income per return across all groups",
   "average taxable income per return for each agi group",
   "average taxable income (per resident) per state",
   "average taxable income per return across all groups",
   "average taxable income per return for each agi group",
   "average dependents per return for each agi group",
   "percentage of returns with no taxable income per agi group",
   "average taxable income per resident",
   "percentage of returns for each agi_group",
   "percentage of taxable income for each agi_group"
 ]
 
def answertxt(state_code):
  '''calls functions to write onto a txt file'''
  fname =  "answers" + state_code + ".txt"
  f =  open(fname, "w")
  #1
  f.write(answer_header(1, question_labels))
  f.write("${:8.0f}".format(avgtax_income_national()))

  #2
  f.write(answer_header(2, question_labels))
  for group in range(1,7):
    f.write("Group " + str(group) + ": ${:8.0f}".format(avgtax_income_per_group(str(group))) + "\n")

  #3
  f.write(answer_header(3, question_labels))
  for state in states_income_dict:
    f.write(state + ": ${:8.0f}".format(states_income_dict[state]['average']) + "\n")

  #name header
  f.write("="*60 + "\n")
  f.write("State level information for " + get_state_name(statetitle, state_code) + "\n")
  f.write("="*60 + "\n")

  #4
  f.write(answer_header(4, question_labels))
  f.write("${:8.0f}".format(avgtax_income_per_return_state(state_code)) + "\n")

  #5
  f.write(answer_header(5, question_labels))
  for group in range(1,7):
    f.write("Group " + str(group) + ": ${:8.0f}".format(avgtax_income_per_return_state_group(state_code, str(group))) + "\n")
  
  #6
  f.write(answer_header(6, question_labels))
  for group in range(1,7):
    f.write("Group " + str(group) + ": {:8.2f}".format(avgtax_dependents_per_return_state_group(state_code, str(group))) + "\n")
  
  #7
  f.write(answer_header(7, question_labels))
  for group in range(1,7):
    f.write("Group " + str(group) + ": {:8.2f}%".format(perc_of_returns_no_taxincome_state_group(state_code, str(group))) + "\n")

  #8
  f.write(answer_header(8, question_labels))
  f.write("${:8.0f}".format(avgtax_income_per_resident_state(state_code)) + "\n")

  #9
  f.write(answer_header(9, question_labels))
  for group in range(1,7):
    f.write("Group " + str(group) + ": {:8.2f}%".format(perc_returns_state_group(state_code, str(group))) + "\n")

  #10
  f.write(answer_header(10, question_labels))
  for group in range(1,7):
    f.write("Group " + str(group) + ": {:8.2f}%".format(perc_taxincome_state_group(state_code, str(group))) + "\n")


######################################################
  #state level data visualization 
######################################################
def pie_percent_returns(state):
  '''create pie chart for percentage of returns for each agi_group'''
  g1 = perc_returns_state_group(state,"1")
  g2 = perc_returns_state_group(state,"2")
  g3 = perc_returns_state_group(state,"3") 
  g4 = perc_returns_state_group(state,"4")
  g5 = perc_returns_state_group(state,"5")
  g6 = perc_returns_state_group(state,"6")

  labels = "G1", "G2", "G3", "G4", "G5", "G6"
  piecontent1 = [g1, g2, g3, g4, g5, g6]
  fig1, ax1 = plt.subplots()
  ax1.pie(piecontent1, explode= None, labels=labels, autopct='%1.1f%%',
  shadow=True, startangle=0)
  ax1.axis('equal')  
  plt.savefig(  "pie1_" + state + ".png")


def pie_perc_taxincome(state):
  '''create pie chart for percentage of taxable income for each agi_group'''
  g1 = perc_taxincome_state_group(state,"1")
  g2 = perc_taxincome_state_group(state,"2")
  g3 = perc_taxincome_state_group(state,"3") 
  g4 = perc_taxincome_state_group(state,"4")
  g5 = perc_taxincome_state_group(state,"5")
  g6 = perc_taxincome_state_group(state,"6")
 
  labels = "G1", "G2", "G3", "G4", "G5", "G6"
  piecontent2 = [g1, g2, g3, g4, g5, g6]
  fig1, ax1 = plt.subplots()
  ax1.pie(piecontent2, explode= None, labels=labels, autopct='%1.1f%%',
  shadow=True, startangle=0)
  ax1.axis('equal')  
  plt.savefig(  "pie2_" + state + ".png")

  return


######################################################
  #national level data visualization 
######################################################

def bar_graph(avgtax_dict):
  '''creates bar graph average taxable income (per resident) for every state'''
  data = avgtax_dict
  values_sorted = sorted(data.items(), key=lambda items: items[1]['average'], reverse=True)
  dict_sorted = dict(values_sorted)
  fig, chart = plt.subplots()

  for keys in dict_sorted:
    chart.bar(keys, dict_sorted[keys]['average'], width = 0.2, align = "edge")
  chart.set_ylabel('average taxable income')
  chart.set_xlabel('state')
  chart.set_title('average taxable income (per resident) per state')

  plt.savefig('bar1.png')
  
######################################################
  #main function
######################################################

def main():
  '''calls all functions in accordance to input'''
  state = input("give me a state code, caps lock pls ")
  answertxt(state)
  pie_percent_returns(state)
  pie_perc_taxincome(state)
  bar_graph(states_income_dict)

main()