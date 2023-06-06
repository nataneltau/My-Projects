package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public class Fighter extends MyBattleSpaceship{
	
	protected static final int BASE_ANNUAL_MAINTENANCE_COST_FIGHTER=2500;
	private static final int COST_FOR_SPACESHIP_ENGINES=1000;
	
	public Fighter(String name, int commissionYear, float maximalSpeed, Set<? extends CrewMember> crewMembers, List<Weapon> weapons){
		super(name, commissionYear, maximalSpeed, crewMembers, weapons);
	}//end of constructor
	
	//Methods

	public int getAnnualMaintenanceCost() {
		int sum;
		
		sum = getWeaponCost();
		sum+= (int)(COST_FOR_SPACESHIP_ENGINES*this.getMaximalSpeed());
		sum+=BASE_ANNUAL_MAINTENANCE_COST_FIGHTER;
		
		return sum;
		
	}//end of method getAnnualMaintenanceCost
	
	@Override
	public String toString() {
		String str;
		
		str ="Fighter\n"+ callToMyBattleSpaceshipToString();
		
		return str;
	}//end of method toString
	
	protected String callToMyBattleSpaceshipToString() {
		return super.toString();
	}
	
}//end of class Fighter
