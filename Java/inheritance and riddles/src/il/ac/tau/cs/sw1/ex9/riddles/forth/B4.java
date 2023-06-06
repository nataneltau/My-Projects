package il.ac.tau.cs.sw1.ex9.riddles.forth;

import java.util.Iterator;

public class B4 implements Iterator<String>{
	
	String[] str;
	int _k;
	int index;
	
	
	public B4(String[] strArr, int k) {
		str = strArr;
		_k =k-1;
		index =0;
	}
	
	public boolean hasNext() {

		if(index<str.length) {
			return true;
		}
		if(_k==0) {
			return false;
		}
		_k--;
		index = 0;		
		
		return true;
		
		
	}
	
	
	public String next() {
		String st = str[index];
		index++;
		return st;
	}
	
}
