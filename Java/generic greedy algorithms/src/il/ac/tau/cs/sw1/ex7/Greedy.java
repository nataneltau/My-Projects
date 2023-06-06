package il.ac.tau.cs.sw1.ex7;

import java.util.*;


public interface Greedy<T>{

    /**
     * A selection function, which chooses the best candidate to be added to the solution
     */
    Iterator<T> selection();

    /**
     * A feasibility function, that is used to determine if a candidate can be used to contribute to a solution
     */
    boolean feasibility(List<T> lst, T element);

    /**
     * An assign function, which assigns a value to a solution, or a partial solution
     */
    void assign(List<T> lst, T element);

    /**
     * A solution function, which will indicate when we have discovered a complete solution
     */
    boolean solution(List<T> lst);

    /**
     * The Greedy Algorithm
     */
    default List<T> greedyAlgorithm(){
    	//declaration of variables
    	Iterator t;
    	T var;
    	List<T> lst = new ArrayList<T>();
    	
    	if(selection()==null)
    		return null;
    	
    	t = selection();

    	while(t.hasNext()) {
    		var = (T)t.next();
    		
    		if(feasibility(lst, var)) {
    			assign(lst, var);
    			
    		}//end of if
    		
    		if(solution(lst)) {
    			return lst;
    		}//end of if
    		
    		
    	}//end of while
    	
    	
    	
        return lst;
    }
}
