package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Set;

public interface Spaceship extends Comparable<Spaceship>{
	
	String getName();
	
	int getCommissionYear();
	
	float getMaximalSpeed();
	
	int getFirePower();
	
	Set<? extends CrewMember> getCrewMembers();
	
	int getAnnualMaintenanceCost();
	
	@Override
	default int compareTo(Spaceship other) {
		int temp1, temp2, res;
		String str1, str2;
		
		temp1 = this.getFirePower();
		temp2 = other.getFirePower();
		res = (-1)*Integer.compare(temp1, temp2);
		
		if(res!=0) 
			return res;
		
		//if we are here, then res==0
		temp1 = this.getCommissionYear();
		temp2 = other.getCommissionYear();
		res = (-1)*Integer.compare(temp1, temp2);
		
		if(res!=0)
			return res;
		
		//if we are here, then res==0
		str1 = this.getName();
		str2 = other.getName();
		
		return str1.compareTo(str2);
		
	}

}
