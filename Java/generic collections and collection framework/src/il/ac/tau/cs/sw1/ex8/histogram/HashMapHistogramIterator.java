package il.ac.tau.cs.sw1.ex8.histogram;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Map;



/**************************************
 *  Add your code to this class !!!   *
 **************************************/
public class HashMapHistogramIterator<T extends Comparable<T>> implements Iterator<T>{
	
	private HashMapHistogramComparator<T> hashComp;
	private Iterator<T> curr;
	
	public HashMapHistogramIterator(Map<T, Integer> map)	{
		
		hashComp = new HashMapHistogramComparator<T>(map);
		
		List<T> lst1 = new ArrayList<T>(map.keySet());
		

		Collections.sort(lst1, hashComp);
		curr= lst1.iterator();
		
	}//end of constructor
	
	@Override
	public boolean hasNext() {
		
		return curr.hasNext();
	}//end of method hasNext

	@Override
	public T next() {
		//your code goes here!
		
		return curr.next(); 
		
	}//end of method next

	@Override
	public void remove() {
		throw new UnsupportedOperationException(); //no need to change this
	}
}
