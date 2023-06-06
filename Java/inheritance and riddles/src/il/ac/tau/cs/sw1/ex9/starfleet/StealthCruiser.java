package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class StealthCruiser extends Fighter {

	private static final Weapon DEFAULT_WEAPON = new Weapon("Laser Cannons", 10, 100);
	private static final int MAINTENANCE_COST_STEALTH_ENGINE = 50;
	private static int numOfElements=0;

	public StealthCruiser(String name, int commissionYear, float maximalSpeed, Set<CrewMember> crewMembers,
			List<Weapon> weapons) {

		super(name, commissionYear, maximalSpeed, crewMembers, weapons);
		numOfElements++;
	}// end of constructor

	public StealthCruiser(String name, int commissionYear, float maximalSpeed, Set<CrewMember> crewMembers) {

		this(name, commissionYear, maximalSpeed, crewMembers, getDefaultWeaponAsList());

	}// end of constructor

	// Methods

	private static List<Weapon> getDefaultWeaponAsList() {

		List<Weapon> lst = new ArrayList<>();
		lst.add(DEFAULT_WEAPON);
		return lst;

	}// end of method getDefaultWeaponAsList

	@Override
	public int getAnnualMaintenanceCost() {
		int sum;
		
		sum = super.getAnnualMaintenanceCost();
		sum+= numOfElements*MAINTENANCE_COST_STEALTH_ENGINE;
		
		return sum;
		
	}// end of method getAnnualMaintenanceCost
	
	@Override
	public String toString() {
		String str;
		
		str = "StealthCruiser\n"+callToMyBattleSpaceshipToString();
		
		return str;
	}//end of method toString

}// end of class StealthCruiser
