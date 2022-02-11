import pandas as pd
from tqdm import tqdm
import spacy
from spacy.matcher import Matcher 
from spacy.tokens import Span 
from nltk.corpus import stopwords
# python -m nltk.downloader stopwords -> terminal에서 실행해 줘야 한다.

nlp = spacy.load('en_core_web_sm')

# Entity extraction
def get_entities(sent, com_name):
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""
  
  for tok in nlp(sent):
    # if token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":
      # check: token is a compound word or not
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      if tok.dep_.find("subj") == True:
        
        ent1 = prefix +" "+ tok.text

        # check ent1 contains company name
        if com_name in ent1.lower():
          ent1 = com_name

        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      if tok.dep_.find("obj") == True:
        
        ent2 = prefix +" "+ tok.text
        
        # check ent2 contains 'tesla' of 'TSLA'
        if com_name in ent2.lower():
          ent2 = com_name
          
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = "" 
        
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text

  # Make the empty string to None
  ent1 = ent1.strip().lower()
  ent2 = ent2.strip().lower()

  if ent1 == "" or ent2 == "":
    ent1 = None
    
  return [ent1, ent2]

# Relation extraction
def get_relation(sent):
  doc = nlp(sent)

  # Matcher class object 
  matcher = Matcher(nlp.vocab)

  #define the pattern 
  pattern = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}] 

  matcher.add("matching_1", [pattern], on_match=None) 

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]] 

  return(span.text.lower())

# Relation Lemmatizer
def relation_lemmatizer(relations):
  lem_relations = []
  lem_word = ""

  for word in relations:
    doc = nlp(word)
    cnt = 0
    
    # showed -> show 뿐만 아니라 showed off -> show off 까지도
    for token in doc:
      if cnt == 0:
        lem_word = token.lemma_
      else:
        lem_word += " " + token.lemma_
      cnt += 1

    lem_relations.append(lem_word)
    
  return lem_relations

def company_re(com_name):
    # number of news
    num_news = 1000
    com_name = com_name.lower()

    # 1. read csv file
    file_path = './rule_base_datasets/' + com_name + '.csv'
    com_data = pd.read_csv(file_path, engine='python')
    
    com_body = com_data['body']
    # 1.2. duplicate the same news
    com_body = com_body.drop_duplicates()

    # 2. entity extractions
    entity_pairs = []
    for sent in tqdm(com_body[:num_news]):
        # get entity pairs -> def get_entities(sent, com_name):
        entity_pairs.append(get_entities(sent, com_name))

    # 3. relation extractions -> def get_relation(sent):
    relations = [get_relation(sent) for sent in tqdm(com_body[:num_news])]
    # relation lemmatization -> def relation_lemmatizer(relations):
    relations = relation_lemmatizer(relations)

    # 4. making DataFrame
    head = [str(ent[0]) for ent in entity_pairs]
    tail = [str(ent[1]) for ent in entity_pairs]
    df = pd.DataFrame({'head':head, 'relation':relations, 'tail':tail})

    # 4.1. remove the rows which contain 'None'
    com_df = pd.DataFrame()
    stop_words = set(stopwords.words('english')) 
    
    for i in range(len(df)):
        if df['head'][i] == 'None' or df['tail'][i] == 'None' or df['relation'][i] == None:
            pass
        elif df['head'][i] in stop_words or df['tail'][i] in stop_words:
            pass
        else:
            com_df = com_df.append({'head': df['head'][i], 'relation': df['relation'][i], 'tail': df['tail'][i]}, ignore_index=True)
        
    # 4.2. add root relation
    com_root = pd.DataFrame([{'head': com_name, 'relation': 'root', 'tail': com_df['head'][i]} for i in range(len(com_df))])

    # 4.3. concatenate the root relation
    com_df = pd.concat([com_df, com_root], ignore_index=True)
    save_path = './rule_base_datasets/results/rule_base_re_' + com_name + '.csv'
    com_df.to_csv(save_path)

    return com_df

def rule_df(com_list):
  df = pd.DataFrame()

  for com_name in com_list:
    com_df = company_re(com_name)
    df = pd.concat([df, com_df], ignore_index=True)
  
  return df