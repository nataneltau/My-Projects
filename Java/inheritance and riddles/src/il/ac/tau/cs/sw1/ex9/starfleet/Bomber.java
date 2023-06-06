package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public class Bomber extends MyBattleSpaceship {

	private static final int BASE_ANNUAL_MAINTENANCE_COST_BOMBER=5000;
	private int _numberOfTechnicians;
	
	public static void main(String[] args) {
		System.out.println("Hello wwww");
	}

	public Bomber(String name, int commissionYear, float maximalSpeed, Set<CrewMember> crewMembers, List<Weapon> weapons, int numberOfTechnicians){
	
		super(name, commissionYear, maximalSpeed, crewMembers, weapons);
		_numberOfTechnicians=numberOfTechnicians;
		
	}//end of constructor
	
	//Methods
	
	public int getNumberOfTechnicians() {
		
		return _numberOfTechnicians;
		
	}//end of method getNumberOfTechnicians
	
	public int getAnnualMaintenanceCost() {
		int sum, temp1;
		double temp2;
		
		temp1 = getWeaponCost();
		
		temp2 = getNumberOfTechnicians();
		temp2*= (1/10.0);
		temp2 = 1-temp2;

		
		sum = (int)(temp1*temp2);
		sum+=BASE_ANNUAL_MAINTENANCE_COST_BOMBER;
		
		return sum;
		
	}//end of method getAnnualMaintenanceCost

	@Override
	public String toString() {
		String str;
		
		str = "Bomber\n"+super.toString()+
				"\n\tNumberOfTechnicians="+getNumberOfTechnicians();
		
		return str;
	}//end of method toString

}//end of class Bomber
