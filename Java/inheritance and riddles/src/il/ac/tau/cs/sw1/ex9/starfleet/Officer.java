package il.ac.tau.cs.sw1.ex9.starfleet;

public class Officer extends CrewWoman implements Comparable<Officer>{
	
	private OfficerRank _rank;
		
	public Officer(String name, int age, int yearsInService, OfficerRank rank) {
		super(age, yearsInService, name);
		_rank = rank;
	}
	
	public OfficerRank getRank() {
		return _rank;
	}//end of method getRank
	
	@Override
	public int compareTo(Officer other) {
		
		return this.getRank().compareTo(other.getRank());
		
	}//end of method compareTo
	
}
