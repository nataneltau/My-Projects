package il.ac.tau.cs.sw1.ex8.histogram;

import java.util.Collection;
import java.util.*;
import java.util.Iterator;
import java.util.Set;

/**************************************
 * Add your code to this class !!! *
 **************************************/
public class HashMapHistogram<T extends Comparable<T>> implements IHistogram<T> {

	private Map<T, Integer> _map;

	public HashMapHistogram() {

		_map = new HashMap<T, Integer>();

	}// end of constructor

	@Override
	public Iterator<T> iterator() {

		Iterator<T> it = new HashMapHistogramIterator<T>(_map);

		return it;
	}

	@Override
	public void addItem(T item) {

		adder(item, 1);

	}// end of method addItem

	/**
	 * @pre amount>=1
	 * @param item
	 * @param amount
	 */
	private void adder(T item, int amount) {
		// declaration of variables
		int num;

		if (_map.containsKey(item)) {
			num = _map.get(item) + 1;
			_map.put(item, num);
		} //end of if
		
		else {
			_map.put(item, 1);
		}//end of else

		
		if(amount==1) {
			return;//we already added 1 item
		}//end of if
		
		num = amount-2+1;
		num+=_map.get(item);//item in _map cause he was there or we put him there at the start of adder
		_map.put(item, num);
		
	}// end of private method adder

	@Override
	public void removeItem(T item) throws IllegalItemException {

		if (!_map.containsKey(item)) {// item not in _map
			throw new IllegalItemException();
		} // end of if

		remover(item, 1);

	}// end of method removeItem

	/**
	 * @pre _map.get(item)<=amount
	 * @pre item in _map
	 * @param item   - the item to remove
	 * @param amount - the amount of item to remove from _map
	 */
	private void remover(T item, int amount) {

		int num;

		num = _map.get(item);
		
		if(num-amount==0) {//should remove the item completely
			_map.remove(item);
			return;
			
		}//end of if
		
		//amount < _map.get(item)
		num-= amount;
		_map.put(item, num);

	}// end of remover

	@Override
	public void addItemKTimes(T item, int k) throws IllegalKValueException {

		if (k < 1) {// illegal

			throw new IllegalKValueException(k);

		} // end of if
			// k>=1 we can add item k times to _map
		adder(item, k);

	}// end of method addItemKTimes

	@Override
	public void removeItemKTimes(T item, int k) throws IllegalItemException, IllegalKValueException {

		if (!_map.containsKey(item)) {// item not in _map

			throw new IllegalItemException();

		} // end of if

		if (_map.get(item) < k || k < 1) {

			throw new IllegalKValueException(k);

		} // end of if

		remover(item, k);

	}// end of method removeItemKTimes

	@Override
	public int getCountForItem(T item) {

		if (!_map.containsKey(item)) {
			return 0;

		} // end of if

		return _map.get(item); // value of item

	}// end of method getCountForItem

	@Override
	public void addAll(Collection<T> items) {
		// declaration of variables
		Iterator<T> it;
		T item;

		it = items.iterator();

		while (it.hasNext()) {

			item = it.next();
			this.addItem(item);

		} // end of while

	}// end of method addAll

	@Override
	public void clear() {

		_map.clear();

	}// end of method clear

	@Override
	public Set<T> getItemsSet() {

		return _map.keySet();

	}// end of method getItemsSet

	@Override
	public void update(IHistogram<T> anotherHistogram) {
		// declaration of variables
		Set<T> set;
		int amount;

		set = anotherHistogram.getItemsSet();

		for (T t : set) {
			amount = anotherHistogram.getCountForItem(t);
			
			if(!(amount>0)) {//always should be amount>0 but needed to check cause @pre of adder -> amount>=1
				
				
			}//end of if
			
			else {//did it that way cause the else should happen more time, the processor will work better
				adder(t, amount);
				
			}//end of else
			
		} // end of for

	}// end of method update

}
