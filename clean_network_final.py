# -*- coding: utf-8 -*-
"""clean_network_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jB3URy_G3YFye_28_EexDbF4cxWSjggD
"""

import networkx as nx
import pandas as pd

"""**Clean up the punctuation and make edge list**"""

punctuation = "!#$%&\'()*+,-./:;<=>?@[\]^`{|}~"
file = open('script_s1_e24.txt','r')
file1 = open("char_s1_e24.txt","r")
file3= open('edges_s1_e24.txt','w')
script_lines = file.readlines()
names= file1.readline()
prev=''
for line in script_lines:
  words=line.split()
  if words:
    for i, word in enumerate(words):
      for punc in word:
        if punc in punctuation:
          words[i]=words[i].replace(punc,"")
    first_word=words[0]
    if prev != '':
      file3.write(prev+ " ")
      file3.write(first_word+ "\n")
      print(prev,first_word)
      prev=first_word
    else:
      prev=first_word
      #print("going to next line")
    for ele in names.split():
      #print (ele)
      if(ele not in words[0] and ele in words):
        file3.write(ele+ " ")
        file3.write(first_word+ "\n")
        print(ele, first_word)
  else:
    #print("line empty")
    prev=''
file3.close()

"""**Make graph object and put weight**"""

file = open('edges_s1_all.txt','r')
edges = file.readlines()
default_weight = 1
G = nx.Graph()
for nodes in edges:
    names= nodes.split()
    n0 = names[0]
    n1 = names[1]
    #print(n0,n1)
    if G.has_edge(n0,n1):   
       G[n0][n1]['weight'] += default_weight
    else:
       G.add_edge(n0,n1, weight=default_weight)

G['Monica']['Ross']['weight']

"""**Graph to CSV with weight**"""

weight= nx.to_pandas_edgelist(G)
weight.to_csv('weight_s1_all.csv',header=['Source','Target','Weight'], index=False)

"""**Making Label from Character file**"""

file4 = open("char_s1_all.txt","r")
names= file4.readline()
name=names.split()
multi= set([x for x in name if name.count(x) > 1])
seen = set()
uniq = []
for x in name:
    if x not in seen:
        uniq.append(x)
        seen.add(x)

name_punc=uniq.copy()
for i, chars in enumerate(name_punc): 
  if '_' in chars:
    name_punc[i]=name_punc[i].replace('_'," ")
id = pd.DataFrame({'ID': uniq, 'Label': name_punc})
id.to_csv('label_s1_all.csv', index=False)

"""**Making Label for Names from Nx Graph**"""

ID=[]
Label=[]
for node, x in G.nodes(data=True):
  ID.append(node)
  if '_' in node:
    punc=node.replace('_'," ")
    Label.append(punc)
  else:
    Label.append(node)
id = pd.DataFrame({'ID': ID, 'Label': Label})
id.to_csv('label_s1_all.csv', index=False)

"""**Zipping and downloading folders**"""

from google.colab import files

!zip -r /content/Edges.zip /content/Edges