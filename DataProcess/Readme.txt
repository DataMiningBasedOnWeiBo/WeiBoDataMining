**------------------DataProcess目录结构------------------**

collectWeiboDataByKeyword------------------>python微博爬虫获取网络数据
|   
+---collectWeiboDataByKeyword.py----------->根据关键词收集微博，数据收集类
+---login.py----------->模拟登陆新浪微博
+---mymain.py----------->程序入口
|
NLPIR------------------->java数据预处理
|
.project
.classpath
+---bin
|   ...
|
+---Data-->NLPIR系统核心词库
|   |   BIG2GBK.map
|   |   BIG5.pdat
|   |   BIG5.wordlist
|   |   BiWord.big
|   |   charset.type
|   |   Configure.xml
|   |   CoreDict.pdat
|   |   CoreDict.pos
|   |   CoreDict.unig
|   |   DocExtractor.user
|   |   FieldDict.pdat
|   |   FieldDict.pos
|   |   GBK.pdat
|   |   GBK.wordlist
|   |   GBK2BIG.map
|   |   GBK2GBKC.map
|   |   GBK2UTF.map
|   |   GBKA.pdat
|   |   GBKA.wordlist
|   |   GBKA2UTF.map
|   |   GBKC.pdat
|   |   GBKC.wordlist
|   |   GBKC2GBK.map
|   |   GranDict.pdat
|   |   GranDict.pos
|   |   ICTPOS.map
|   |   location.map
|   |   location.pdat
|   |   location.wordlist
|   |   NewWord.lst
|   |   NLPIR.ctx
|   |   NLPIR.user
|   |   NLPIR_First.map
|   |   nr.ctx
|   |   nr.fsa
|   |   nr.role
|   |   PKU.map
|   |   PKU_First.map
|   |   sentiment.pdat
|   |   sentiment.ung
|   |   UserDict.pdat
|   |   UTF2GBK.map
|   |   UTF2GBKA.map
|   |   UTF8.pdat
|   |   UTF8.wordlist
|   |   
|   \---English-->英文处理的支持知识库，如果不需要英文处理的功能，可以不加载本库。
|           English.pdat
|           English.pos
|           English.ung
|           English.wordlist
|           Irrel2regular.map
|           ne.pdat
|           ne.pos
|           ne.wordlist
|
+---dict-------->用户词典
|   |   emotion.txt 情感词典
|   |   expression.txt 表情符号及网络词典，已导入
|   |   user_dict.txt 测试使用字典
|   |   
|   \---table-->停用词表和情感词表
|           StopWordTable.txt
|           EmotionWordTable.txt
|
+---dll-------->NLPIR 不同环境下的支撑库
|   +---linux32-->Linux 32bit操作系统下的支持库
|   |       NLPIR.so
|   |       
|   +---linux64-->Linux 64bit操作系统下的支持库
|   |       NLPIR.so
|   |       
|   +---win32-->Win 32bit操作系统下的支持库
|   |       NLPIR.dll
|   |       
|   \---win64-->Win 64bit操作系统下的支持库
|           NLPIR.dll
|
+---lib-------->所需jar包
|   ...
|
+---src-------->主要代码
|   +---com.nlpir
|   |   +---demo
|   |   |       NlpirLib.java
|   |   |       NlpirMethod.java
|   |   +---test
|   |   |       NlpirTest.java
|   |   +---util
|   |   |       OSInfo.java
|   |   \---Impl
|   |           SegmentImpl.java------>调用nlpir接口进行分词处理
|

**------------------------------------------------------**
