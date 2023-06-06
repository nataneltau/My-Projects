package il.ac.tau.cs.sw1.ex9.starfleet;

public class Cylon extends MyCrewMember {

	private int _modelNumber;
	
	public Cylon(String name, int age, int yearsInService, int modelNumber) {
		super(age, yearsInService, name);
		_modelNumber = modelNumber;
		
	}
	
	
	public int getModelNumber() {
		return _modelNumber;
	}//end of method getModelNumber
	
	
}
