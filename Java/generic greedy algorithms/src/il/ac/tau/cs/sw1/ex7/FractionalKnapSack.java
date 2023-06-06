package il.ac.tau.cs.sw1.ex7;
import java.util.*;

public class FractionalKnapSack implements Greedy<FractionalKnapSack.Item>{
    int capacity;
    List<Item> lst;

    FractionalKnapSack(int c, List<Item> lst1){
        capacity = c;
        lst = lst1;
    }

    public static class Item {
        double weight, value;
        Item(double w, double v) {
            weight = w;
            value = v;
        }

        @Override
        public String toString() {
            return "{" + "weight=" + weight + ", value=" + value + '}';
        }
    }

    @Override
    public Iterator<Item> selection() {
    	sorti(lst);
        return this.lst.iterator();
    }
    

    private static void sorti(List<Item> items) {
    	//declaration of variables
    	Item[] arr = new Item[items.size()];
    	
    	
    	for(int i=0; i<arr.length; i++) {
    		
    		arr[i] = items.get(i);
    		
    	}//end of for
    	
    	//sort with bubble sort with the key sort is value/weight
    	bubbleSorti(arr);//bad complex time, dont want improve, still O(n^2) complexity
    	
    	for(int i=0; i<arr.length; i++) {
    		
    		items.set(i, arr[i]);
    		
    	}//end of for
    	
    	
    	
    }//end of private method sorti
    
    private static void bubbleSorti(Item[] arr) {
    	double num1, num2;
    	Item temp;
    	
    	for(int i =0; i<arr.length; i++) {
    		for(int j=0; j<arr.length-i-1; j++) {
    			num1 =arr[j].value/arr[j].weight;
    			num2 =arr[j+1].value/arr[j+1].weight;
    			
    			if(num1<num2) {
    				temp = arr[j];
    				arr[j]=arr[j+1];
    				arr[j+1] = temp;
    				
    				
    				
    			}//end of if
    			
    			
    		}//end of inner for
    		
    		
    	}//end of external for
    	
    }//end of private method bubbleSorti
    

    @Override
    public boolean feasibility(List<Item> candidates_lst, Item element) {
    	
        return capacity - sumWeight(candidates_lst)>0;
    }
    
    private double sumWeight(List<Item> lst) {
    	double sum=0;
    	
    	for(Item it: lst ) {
    		sum +=it.weight;
    		
    	}//end of for
    	
    	return sum;
    	
    }//end of private method sumWeight

    @Override
    public void assign(List<Item> candidates_lst, Item element) {
    	
    	if(sumWeight(candidates_lst)+element.weight<=capacity) {
    		candidates_lst.add(element);
    		return;
    		
    	}//end of if
    	
    	double temp, tempElm;
    	Item it;
    	    	
    	temp = capacity - sumWeight(candidates_lst);//we do it cause: element.weight>capacity-sumWeight(candidates_lst)
    	tempElm = temp / element.weight;
    	tempElm *= element.value;
    	
    	it = new Item(temp, tempElm);
    	
    	candidates_lst.add(it);
    	
    }

    @Override
    public boolean solution(List<Item> candidates_lst) {
    	
        return capacity - sumWeight(candidates_lst)==0;
    }
}
