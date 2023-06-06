package il.ac.tau.cs.sw1.ex8.wordsRank;

import java.util.Comparator;

import il.ac.tau.cs.sw1.ex8.wordsRank.RankedWord.rankType;


/**************************************
 *  Add your code to this class !!!   *
 **************************************/

class RankedWordComparator implements Comparator<RankedWord>{
	
	private boolean isMax, isMin, isAve;
	
	public RankedWordComparator(rankType cType) {
		//i copy the code from getRankByType 
		switch(cType){
		case average:
			isAve = true;
			break;
		case min:
			isMin=true;
			break;
		default: //case max
			isMax=true;
			break;
		}
	}
	
	@Override
	public int compare(RankedWord o1, RankedWord o2) {
		//your code goes here!
		if(isMax ==true) {
			return Integer.compare(o1.getRankByType(rankType.max), o2.getRankByType(rankType.max));
			}//end of if
		
		else if(isMin ==true) {
			return Integer.compare(o1.getRankByType(rankType.min), o2.getRankByType(rankType.min));
		}//end of else if
		
		else if(isAve == true) {
			return Integer.compare(o1.getRankByType(rankType.average), o2.getRankByType(rankType.average));
		}//end of else if
		
		
		return 0; //replace this with the actual returned value
	}//end of method compare
	

}
