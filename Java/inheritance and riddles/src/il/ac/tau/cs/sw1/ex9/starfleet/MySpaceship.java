package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Objects;
import java.util.Set;

public abstract class MySpaceship implements Spaceship {

	private static final int BASIC_FIRE_POWER = 10;
	protected static final int MAINTENANCE_COST_OF_CREW_MEMBER = 500;
	protected String _name;
	protected int _commissionYear;
	protected float _maximalSpeed;
	protected Set<? extends CrewMember> _crewMembers;

	public MySpaceship(String name, int commissionYear, float maximalSpeed, Set<? extends CrewMember> crewMembers) {

		_name = name;
		_commissionYear = commissionYear;
		_maximalSpeed = maximalSpeed;
		_crewMembers = crewMembers;

	}// end of constructor

	// Methods

	public String getName() {

		return _name;

	}// end of method getName

	public int getCommissionYear() {

		return _commissionYear;

	}// end of method getCommissionYear

	public float getMaximalSpeed() {

		return _maximalSpeed;

	}// end of method getMaximalSpeed

	public int getFirePower() {

		return BASIC_FIRE_POWER;

	}// end of method getFirePower

	public Set<? extends CrewMember> getCrewMembers() {

		return _crewMembers;

	}// end of method getCrewMembers

	@Override
	public int hashCode() {
		return Objects.hash(_name);
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (!(obj instanceof MySpaceship))
			return false;
		MySpaceship other = (MySpaceship) obj;
		return Objects.equals(_name, other._name);
	}

	@Override
	public String toString() {
		String str;

		str = "\tName=" + getName() + "\n\tCommissionYear=" + getCommissionYear() + "\n\tMaximalSpeed="
				+ getMaximalSpeed() + "\n\tFirePower=" + getFirePower() + "\n\tCrewMembers=" + getCrewMembers().size()
				+ "\n\tAnnualMaintenanceCost=" + getAnnualMaintenanceCost();

		return str;
	}

}// end of abstract class MySpaceship
