package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public class ColonialViper extends Fighter{

	private static final int BASE_ANNUAL_MAINTENANCE_COST_COLONIAL_VIPER=4000;
	private static final int MAINTENANCE_COST_OF_SPACESHIP_ENGINE=500;
	
	
	public ColonialViper(String name, int commissionYear, float maximalSpeed, Set<CrewWoman> crewMembers,
			List<Weapon> weapons) {
		
		super(name, commissionYear, maximalSpeed, crewMembers, weapons);
		
	}//end of constructor

	//Methods
	
	@Override
	public int getAnnualMaintenanceCost() {
		int sum;
		
		sum = getWeaponCost();
		sum+= BASE_ANNUAL_MAINTENANCE_COST_COLONIAL_VIPER;
		sum+= _crewMembers.size()*MAINTENANCE_COST_OF_CREW_MEMBER;
		sum+= (int)(this.getMaximalSpeed()*MAINTENANCE_COST_OF_SPACESHIP_ENGINE);
		
		return sum;
		
	}//end of method getAnnualMaintenanceCost
	
	@Override
	public String toString() {
		String str;
		
		str = "ColonialViper\n"+callToMyBattleSpaceshipToString();
		
		return str;
	}//end of method toString
	
}//end of class ColonialViper
