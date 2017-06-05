package com.nlpir.impl;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

import net.sf.json.JSONObject;
import org.bson.Document;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.nlpir.demo.NlpirMethod;

public class SegmentImpl {
	
	private static MongoClient mongoClient = new MongoClient("127.0.0.1", 27017);
    private static MongoDatabase db = mongoClient.getDatabase("weiboDB");
    //获取数据源集合
    private static MongoCollection<Document> dataCollection = db.getCollection("crawlerData");
    //分词结果存储集合
    private static MongoCollection<Document> saveCollection = db.getCollection("saveData");
    //分词结果存储路径
	//public static final String outPath = "d:\\outwithnot.txt";
	 //停用词词表
	public static final String stopWordTable = "dict/table/StopWordTable.txt";
	 //情感词汇表
	public static final String emotionWordTable = "dict/table/EmotionWordTable.txt";
	
	
	public static void main(String[] args){
		String keyword = "赵丽颖";
		dataProcess(keyword);
	}
 
	
	public static void dataProcess(String keyword) {
		String content = "";
		String result = "";
		
		try{
			content = getContent(dataCollection, keyword);
			result = matchEmotionWord(fileExcludeStopWord(content));
			savaData(saveCollection, keyword, result);
		} catch(Exception e){
			System.out.println("error: "+e);
		} finally{
			mongoClient.close();
		}
	}
	
	/**
	 * 分词
	 * @param content
	 *            提取的微博内容
	 * @return 分词结果
	 */
	public static String segHandle(String content) {
		//添加用户词典
		NlpirMethod.NLPIR_ImportUserDict("dict/expression.txt", false);
		//调用nlpir分词接口得到分词结果
		String result = NlpirMethod.NLPIR_ParagraphProcess(content, 0);
		//将分词结果写入txt中
		//write2Txt(result, outPath);
		return result;
	}
	
	/**
	 * 去除停用词
	 * @param content
	 *            提取的微博内容
	 * @return 过滤停用词后的分词结果
	 */
	public static String fileExcludeStopWord(String content) {
		StringBuffer finalStr = null;
		BufferedReader StopWordFileBr = null;

		try {
			StopWordFileBr = new BufferedReader(new InputStreamReader(new FileInputStream(new File(stopWordTable)), "UTF-8"));

			Set<String> stopWordSet = new HashSet<String>();
			
			//初始化停用词集
			String stopWord = null;
			for(; (stopWord = StopWordFileBr.readLine()) != null;){
				stopWordSet.add(stopWord);
			}
			
			String result = null;
			String[] resultArray = null;
			try {
				//对读入的文本进行分词
				result = segHandle(content);
				//得到分词后的词汇数组，以便后续比较
				resultArray = result.split(" ");
			} catch(Exception e){
				System.out.println("paragraph error"+e);
			}
			
			//过滤停用词 
			for(int i = 0; i< resultArray.length; i++){
				//System.out.println(resultArray[i]);
				if(stopWordSet.contains(resultArray[i])){
					resultArray[i] = null;
				}
				//System.out.println(resultArray[i]);
			}
				
			//把过滤后的字符串数组存入到一个字符串中
			finalStr = new StringBuffer();
			for(int i = 0; i< resultArray.length; i++){
				if(resultArray[i] != null){
					finalStr = finalStr.append(resultArray[i]).append(" ");
				}
			}
	
			StopWordFileBr.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch(Exception e){
			e.printStackTrace();
		}
		
		return finalStr.toString();
	}
	
	/**
	 * 提取情感词
	 * @param excludeStopWord
	 * 			去除停用词后的文本
	 * @return 包含在情感词汇表中的情感词集合
	 */
	public static String matchEmotionWord(String excludeStopWord) {
		BufferedReader emotionWordFileBr = null;
		StringBuffer resultStr = null;
		
		try {
			emotionWordFileBr = new BufferedReader(new InputStreamReader(new FileInputStream(new File(emotionWordTable)), "UTF-8"));
			//用来存放停用词的集合
			Set<String> emotionWordSet = new HashSet<String>();
			
			//初始化情感词集
			String stopWord = null;
			for(; (stopWord = emotionWordFileBr.readLine()) != null;){
				emotionWordSet.add(stopWord);
			}
			//System.out.println("emotion size: "+emotionWordSet.size());

			String[] wordArray = excludeStopWord.split(" ");
			//System.out.println("wordarray length: "+wordArray.length);
			
			resultStr = new StringBuffer();
			//过滤非情感词,把过滤后的字符串数组存入到一个字符串中
			for(int i = 0; i< wordArray.length; i++){
				//System.out.println(wordArray[i]);
				if(emotionWordSet.contains(wordArray[i])){
					resultStr = resultStr.append(wordArray[i]).append(" ");
					//wordArray[i] = null;
				}
			}
			
			emotionWordFileBr.close();
		} catch(Exception e){
			System.out.print("error "+e);
		}
		
		return resultStr.toString();
	}
	
	/**
	 * 获取评论文本
	 * @param collection
	 * 			指定的数据来源集合
	 * @param keyword
	 * 			关键词
	 * @return 根据关键词查询到的文本集
	 */
	public static String getContent(MongoCollection<Document> collection, String keyword) {
		String weiboContent = "";
		MongoCursor<Document> iterator = null;

        //查询条件
        iterator = collection.find(new Document("keyword",new Document("$eq", keyword))).projection(new Document("content" ,1).append("_id", 0)).iterator();
        try {
            while (iterator.hasNext()) {
                String oneContent = iterator.next().toJson();
                oneContent = oneContent.replaceAll("\\\\n\\\\t\\\\t", "");
                oneContent = oneContent.replaceAll("\\\\u200b", "");
                //oneContent = oneContent.replaceAll("\\s*", "");
                
                JSONObject json = new JSONObject().fromObject(oneContent);
                weiboContent += json.get("content");
                weiboContent = weiboContent.replaceAll("\\s*", "");
                //System.out.println(oneContent);
            }
        } finally {
            iterator.close();
        }
		return weiboContent;
	}
	
	/**
	 * 分词结果存库
	 * @param collection
	 * 			存储至目标集合
	 * @param keyword
	 * 			关键词
	 * @param data
	 * 			分词结果
	 */
	public static void savaData(MongoCollection<Document> collection, String keyword, String data) {
		try {
			Document document = new Document("keyword", keyword).append("words", data).append("date", new Date());
			collection.insertOne(document);
		} catch(Exception e){
			System.out.println("error: "+e);
		}
	}
	
	/**
	 * 分词结果存储至文本文件
	 * @param content
	 * 			存储内容
	 * @param path
	 * 			路径，参见outpath
	 */
	public static void write2Txt(String content, String path) {
		File fp=new File(path);
		PrintStream ps = null;
		try {
			ps = new PrintStream(new FileOutputStream(fp));
			ps.println(content);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			ps.close();
		}
	}
}
