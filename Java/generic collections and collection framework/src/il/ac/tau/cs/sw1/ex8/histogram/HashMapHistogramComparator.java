package il.ac.tau.cs.sw1.ex8.histogram;

import java.util.Comparator;
import java.util.Map;

public class HashMapHistogramComparator<T extends Comparable<T>> implements Comparator<T> {

	private Map<T, Integer> _map;
	
	public HashMapHistogramComparator(Map<T, Integer> map){
		
		_map = map;
		
	}//end of constructor
	
	
	public int compare(T t1, T t2) {
		
		int num1, num2, res;

		num1 = _map.get(t1);
		num2 = _map.get(t2);
		
		res = (-1)*Integer.compare(num1, num2);
		
		if(res==0) {
		
			res = t1.compareTo(t2);
			
		}//end of if
		
		return res;
		
	}//end of method compare
	
}
