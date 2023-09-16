import json
import jieba
import jieba.posseg as pseg
import operator

#繁體中文
jieba.set_dictionary('dict.txt.big')

#From KEM_dic_noun 加入30萬個自訂詞彙
print('load use userdict_ex begins')
jieba.load_userdict('userdict_ex.txt')
print('load use userdict_ex ends 300,000')

#讀取考卷
f = open('questions_example.json', mode = "r", encoding = 'utf-8')
question = json.load(f)

#讀取反向索引表
f3 = open('inverted_index.json', mode = "r", encoding = 'utf-8')
dic_inverted_index = json.load(f3)

#詞性表
#flag_list = ['n','ng','nr','nrfg','nrt','ns','nt','nz']
flag_list = ['n']

#雜訊
ignore_list = ['官方','主權國家','簡稱','首任','校長','定位','大學','目標','綜合大學','改名','現代','學風','省份','省會','人類','生活','距今','中國','亞洲',
               '並稱','分屬','國家','城市','憲法','首都','政府','國王','全世界','語言','地區','總部','從事','行動','生產','成立於','業務','技術','授權',
               '消費者','部門','品牌','製造','跨國公司','通訊設備','頂點','鄰國','人口','國界','原本','全國','中央','地理位置','在一起','能力','相關','產品',
               '中部','中心','城鎮','又稱','景點']
ignore_list2 = ['官方','主權國家','簡稱','首任','校長','定位','大學','目標','綜合大學','改名','現代','學風','省份','省會','人類','生活','距今','中國','亞洲',
               '並稱','分屬','國家','城市','憲法','首都','政府','國王','全世界','語言','地區','總部','從事','行動','生產','成立於','業務','技術','授權',
               '消費者','部門','品牌','製造','跨國公司','通訊設備','頂點','鄰國','人口','國界','原本','全國','中央','地理位置','在一起','能力','相關','產品',
               '中部','中心','城鎮','又稱','景點',
               '東北','西南','服務','基礎','通信','遷都','國土','海港','西岸','市為']
ignore_list3 = ['官方','主權國家','簡稱','首任','校長','定位','大學','目標','綜合大學','改名','現代','學風','省份','省會','人類','生活','距今','中國','亞洲',
               '並稱','分屬','國家','城市','憲法','首都','政府','國王','全世界','語言','地區','總部','從事','行動','生產','成立於','業務','技術','授權',
               '消費者','部門','品牌','製造','跨國公司','通訊設備','頂點','鄰國','人口','國界','原本','全國','中央','地理位置','在一起','能力','相關','產品',
               '中部','中心','城鎮','又稱','景點',
               '東北','西南','服務','基礎','通信','遷都','國土','海港','西岸','市為',
               '方面']
ignore_list4 = ['官方','主權國家','簡稱','首任','校長','定位','大學','目標','綜合大學','改名','現代','學風','省份','省會','人類','生活','距今','中國','亞洲',
               '並稱','分屬','國家','城市','憲法','首都','政府','國王','全世界','語言','地區','總部','從事','行動','生產','成立於','業務','技術','授權',
               '消費者','部門','品牌','製造','跨國公司','通訊設備','頂點','鄰國','人口','國界','原本','全國','中央','地理位置','在一起','能力','相關','產品',
               '中部','中心','城鎮','又稱','景點',
               '東北','西南','服務','基礎','通信','遷都','國土','海港','西岸','市為',
               '方面',
               '非洲']
ignore_list5 = ['官方','主權國家','簡稱','首任','校長','定位','大學','目標','綜合大學','改名','現代','學風','省份','省會','人類','生活','距今','中國','亞洲',
               '並稱','分屬','國家','城市','憲法','首都','政府','國王','全世界','語言','地區','總部','從事','行動','生產','成立於','業務','技術','授權',
               '消費者','部門','品牌','製造','跨國公司','通訊設備','頂點','鄰國','人口','國界','原本','全國','中央','地理位置','在一起','能力','相關','產品',
               '中部','中心','城鎮','又稱','景點',
               '東北','西南','服務','基礎','通信','遷都','國土','海港','西岸','市為',
               '方面',
               '非洲',
               '美國','致力於','戰爭','實現','合作']

#空白答案卷     
answer_list=[]

#QAbot function
def QAbot(q):
    dic_intersection = {'A' : 0, 'B' : 0, 'C' : 0 }
    dic_check={}
    
    listA=[]
    listB=[]
    listC=[]

    #建立答案選項的出現文章清單
    print('********A********')
    if q['A'] in dic_inverted_index.keys():
        listA=dic_inverted_index[q['A']]
    else:
        print('A. '+ q['A'] +' not in inverted index')
    #print(listA)
    print('********B********')
    if q['B'] in dic_inverted_index.keys():
        listB=dic_inverted_index[q['B']]
    else:
        print('B. '+ q['B'] +' not in inverted index')
    #print(listB)
    print('********C********')
    if q['C'] in dic_inverted_index.keys():
        listC=dic_inverted_index[q['C']]
    else:
        print('C. '+ q['C'] +' not in inverted index')
    #print(listC)

    #斷詞並開始分析句子中目標詞彙與答案選項之交集關係
    print('Check Sentence:')
    words=pseg.cut(q['Question'])
    for word in words:
        if word.word not in dic_check.keys() and word.flag in flag_list and len(word.word)!=1 and word.word not in ignore_list5:
            print(word.word)

            target_word = word.word
            if target_word == '西非國家':
                print('西非國家->西非')
                target_word = '西非'

            dic_check[target_word]=1

            #檢查目標詞彙是否在反向索引表內，並查該目標詞彙出現在哪些文章
            list_word=[]
            if target_word in dic_inverted_index.keys():
                list_word=dic_inverted_index[target_word]
            else:
                print(target_word+'not in inverted index')
            #print(list_word)
            
            #檢查目標詞彙與答案選項是否交集，每交集一篇文章，則+1
            for id in list_word:
                if id in listA:
                    dic_intersection['A']+=1
                if id in listB:
                    dic_intersection['B']+=1
                if id in listC:
                    dic_intersection['C']+=1

    #秀出每一個答案選項所獲得的交集總數
    print('A:',dic_intersection['A'])
    print('B:',dic_intersection['B'])
    print('C:',dic_intersection['C'])
    
    #取交集總數最高者為答案
    max_key = max(dic_intersection, key=lambda key: dic_intersection[key])
    answer_list.append(max_key)

#測時只跑一題
# QAbot(question[10])

#執行QAbot去跑一整份試卷
count=0
for q in question:
    count+=1
    print('Question',count,'start!')
    QAbot(q)    
    print('Question',count,'finished!')
    print('=================')
    # if count == 5:
    #     break

#秀出答案
print(answer_list)

#將答案寫成json格式
with open('answer_list.json', 'w', encoding='utf-8') as f2:
  f2.write(json.dumps(answer_list, sort_keys=True, indent=4,ensure_ascii=False))
  f2.write('\n')

#關檔
f.close()
f2.close()
f3.close()