package il.ac.tau.cs.sw1.ex8.wordsRank;

import java.io.BufferedReader;
import java.util.*;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import il.ac.tau.cs.sw1.ex8.histogram.HashMapHistogram;
import il.ac.tau.cs.sw1.ex8.histogram.HashMapHistogramComparator;
import il.ac.tau.cs.sw1.ex8.histogram.IHistogram;
import il.ac.tau.cs.sw1.ex8.wordsRank.RankedWord.rankType;

/**************************************
 * Add your code to this class !!! *
 **************************************/

public class FileIndex {

	public static final int UNRANKED_CONST = 30;
	private HashMapHistogram<String>[] _histogram;
	private String[] _files;
	private Map<String, Integer>[] _ranks;
	private int _index;
	private String _folderName;

	/*
	 * @pre: the directory is no empty, and contains only readable text files
	 */
	public void indexDirectory(String folderPath) {
		// This code iterates over all the files in the folder. add your code wherever
		// is needed
		// declaration of variables
		String fileName, variable;
		File folder = new File(folderPath);
		File[] listFiles = folder.listFiles();
		List<String> theTokens = new LinkedList<>();
		Iterator<String> it;
		int len;

		len = listFiles.length;
		
		_folderName = folderPath;
		_index = -1;
		_histogram = new HashMapHistogram[len];
		_files = new String[len];
		_ranks = new Map[len];

		createHistograms(_histogram);

		for (File file : listFiles) {
			// for every file in the folder
			if (file.isFile()) {
				try {
					theTokens = FileUtils.readAllTokens(file);
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				fileName = file.toString();
				it = theTokens.iterator();

				_index++;

				_files[_index] = fileName;

				while (it.hasNext()) {
					variable = it.next();
					_histogram[_index].addItem(variable);
				} // end of while

			} // end of if

		} // end of for

		for (int i = 0; i < _files.length; i++) {
			makeRanks(_histogram[i], i);
		} // end of for

	}// end of method indexDirectory

	private static void createHistograms(HashMapHistogram[] hist) {

		for (int i = 0; i < hist.length; i++) {

			hist[i] = new HashMapHistogram<String>();

		} // end of for

	}// end of private method createHistograms

	private void makeRanks(HashMapHistogram<String> hist, int ind) {
		// declaration of variables
		String word;
		int num;
		Iterator<String> it;

		_ranks[ind] = new HashMap<String, Integer>();
		it = hist.iterator();
		num = 1;

		while (it.hasNext()) {
			word = it.next();
			_ranks[ind].put(word, num);
			num++;

		} // end of while

	}// end of private method makeRanks

	/*
	 * @pre: the index is initialized
	 * 
	 * @pre filename is a name of a valid file
	 * 
	 * @pre word is not null
	 */
	public int getCountInFile(String filename, String word) throws FileIndexException {
		// your code goes here!
		int location;

		location = searchWhichFile(filename);

		if (location == -1)
			exceptionMessage();

		word = word.toLowerCase();

		return _histogram[location].getCountForItem(word);

	}// end of method getCountInFile

	private int searchWhichFile(String filename) {
		int location = -1;
		String search;

		search = _folderName + File.separator + filename;

		for (int i = 0; i <= _index; i++) {
			if (search.equals(_files[i])) {
				return location = i;

			} // end of if
		} // end of for

		return location;
	}// end of private

	private static void exceptionMessage() throws FileIndexException {

		throw new FileIndexException("File don't exist");

	}// end of private method exceptionMessage

	/*
	 * @pre: the index is initialized
	 * 
	 * @pre filename is a name of a valid file
	 * 
	 * @pre word is not null
	 */
	public int getRankForWordInFile(String filename, String word) throws FileIndexException {
		// declaration of variables
		int location;

		location = searchWhichFile(filename);

		if (location == -1)// file don't exist
			exceptionMessage();

		return getRankForWordInSpecificFile(location, word);

	}// end of method getRankForWordInFile

	private int getRankForWordInSpecificFile(int locationInFiles, String word) {

		word = word.toLowerCase();

		if (_histogram[locationInFiles].getCountForItem(word) == 0) {// word not in file
			return wordNotExistInRanksMethods(locationInFiles);
		} // end of if

		return _ranks[locationInFiles].get(word);

	}// end of private method getRankForWordInSpecificFile

	private int wordNotExistInRanksMethods(int location) {
		Set<String> set = _histogram[location].getItemsSet();

		return set.size() + UNRANKED_CONST;

	}// end of private method wordNotExistInRanksMethods

	/*
	 * @pre: the index is initialized
	 * 
	 * @pre word is not null
	 */
	public int getAverageRankForWord(String word) {

		return getRankForWordFolder(rankType.average, word);

	}// end of method getAverageRankForWord

	private int getRankForWordFolder(rankType type, String word) {
		// declaration of variables
		Map<String, Integer> mapOfFiles = new HashMap<String, Integer>();
		int num;
		String fileName;
		RankedWord rw;

		for (int i = 0; i < _ranks.length; i++) {

			num = getRankForWordInSpecificFile(i, word);
			fileName = _files[i];
			mapOfFiles.put(fileName, num);

		} // end of for

		word = word.toLowerCase();

		rw = new RankedWord(word, mapOfFiles);

		return rw.getRankByType(type);

	}// end of private method getRankForWordFolder

	private List<String> getRankForTheKMethods(rankType type, int k) {//prevent code duplication in the k's methods
		// declaration of variables
		int ave;
		Set<String> set = new HashSet<String>();
		String word;
		Map<String, Integer> map = new HashMap<String, Integer>();

		for (int i = 0; i < _ranks.length; i++) {

			for (Map.Entry<String, Integer> entry : _ranks[i].entrySet()) {

				word = entry.getKey();

				if (!(set.contains(word))) {

					ave = getRankForWordFolder(type, word);

					if (ave < k) {

						map.put(word, ave);

					} // end of inner if

					set.add(word);

				} // end of if

			} // end of inner for

		} // end of for

		// that I copy from HashMapHistogramIterator
		MyComparator comp = new MyComparator(map);

		List<String> lst1 = new ArrayList<String>(map.keySet());

		Collections.sort(lst1, comp);

		return lst1;

	}// end of private method getRankForTheKMethods

	public List<String> getWordsWithAverageRankSmallerThanK(int k) {

		return getRankForTheKMethods(rankType.average, k);

	}// end of method getWordsWithAverageRankSmallerThanK

	public List<String> getWordsWithMinRankSmallerThanK(int k) {

		return getRankForTheKMethods(rankType.min, k);

	}// end of method getWordsWithMinRankSmallerThanK

	public List<String> getWordsWithMaxRankSmallerThanK(int k) {

		return getRankForTheKMethods(rankType.max, k);

	}// end of method getWordsWithMaxRankSmallerThanK

	public class MyComparator implements Comparator<String> {// very similar to HashMapHistogramComparator

		private Map<String, Integer> mapComp;

		public MyComparator(Map<String, Integer> map) {

			mapComp = map;

		}// end of constructor

		public int compare(String word1, String word2) {
			int num1, num2;

			num1 = mapComp.get(word1);
			num2 = mapComp.get(word2);

			return Integer.compare(num1, num2);
		}// end of method compare

	}// end of class MyComparator

}// end of class FileIndex
