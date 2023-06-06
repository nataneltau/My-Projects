package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public abstract class MyBattleSpaceship extends MySpaceship {
	
	protected List<Weapon> _weapons;
	
	public MyBattleSpaceship(String name, int commissionYear, float maximalSpeed, Set<? extends CrewMember> crewMembers, List<Weapon> weapons) {
		
		super(name, commissionYear, maximalSpeed, crewMembers);
		_weapons=weapons;
			
	}//end of constructor
	
	//methods
	
	public List<Weapon> getWeapon(){
		
		return _weapons;
		
	}//end of method getWeapon
	
	@Override
	public int getFirePower() {
		int sum;
		
		sum=getWeaponFirePower();
		
		sum+=super.getFirePower();
		
		return sum;
		
	}//end of method getFirePower
	
	protected int getWeaponFirePower() {
		int sum=0;
		
		for(Weapon w: _weapons) {
			sum+=w.getFirePower();
		}//end of for
		
		return sum;
		
	}//end of protected method getWeaponFirePower
	
	protected int getWeaponCost() {
		int sum=0;
		
		for(Weapon w: _weapons) {
			sum+=w.getAnnualMaintenanceCost();
		}//end of for
		
		return sum;
		
	}//end of protected method getWeaponFirePower
	
	@Override
	public String toString() {
		String str;
		
		str = super.toString()+"\n\tWeaponArray="+_weapons.toString();
		
		return str;
	}//end of method toString

}//end of abstract class MyBattleSpaceship
