import json
import ijson

dic_invert_index={}
flag_list = ['n','ng','nr','nrfg','nrt','ns','nt','nz']
i = 1
appear_times = 0
with open("wiki_tokenize_2021_08_05_1215639.json", mode = "r", encoding = 'utf-8') as file:
    list_json = ijson.parse(file)
    for article in ijson.items(list_json, 'item'):
        for sentence in article['tokens']:
            for vocabulary in sentence:
                if len(vocabulary[0])!=1 and vocabulary[1] in flag_list:
                    if vocabulary[0] not in dic_invert_index.keys():   #善用keys()
                        list = []
                        list.append(article['id'])
                        dic_invert_index[vocabulary[0]]=list  
                    elif article['id'] not in dic_invert_index[vocabulary[0]]:
                        dic_invert_index[vocabulary[0]].append(article['id'])              
        #if i%10==0:
        if i % 1000 == 0:
            print('Article' , i , 'ends')
            #break
        i += 1
file.close()

#print(dic_invert_index)

with open('inverted_index.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(dic_invert_index, sort_keys=True, indent=4,ensure_ascii=False))
  f.write('\n')
f.close()