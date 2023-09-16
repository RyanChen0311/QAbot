# QAbot
### 自然語言處理QAbot

##### 1.使用 inverted_index_build.py 建立反向索引表
##### 2.使用 QAbot.py 讀取反向索引表回答問題

Q:
{  
"Question":  
	"中國戰國時期秦國及秦朝政治人物，  
	歷仕秦始皇、秦二世和秦王子嬰三代君主，  
	沙丘之變和望夷宮之變的主謀、策劃者。  
	最後被子嬰派宦官韓談刺殺而死。。",  
	 "A": "鄭丰", "B": "荊軻", "C": "趙高"  
}  

A:  
	QAbot會利用jieba套件斷詞問題再根據反向索引表回答"C"  
	
原理是利用出現在維基百科的詞頻及與題目斷詞共同出現的文章數量最大的選項為答案  

反向索引表格式如下:  
	"湖時":  
	[  
        259003,  
        640980,  
        702905,  
        720338  
    	],  
上面編號是出現在第259003篇文章，以此類推
