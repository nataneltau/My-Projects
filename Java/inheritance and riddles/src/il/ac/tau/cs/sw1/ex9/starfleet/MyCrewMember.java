package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Objects;

public abstract class MyCrewMember implements CrewMember {

	protected int _age;
	protected int _yearsInService;
	protected String _name;

	
	//constructors
	public MyCrewMember(int age, int yearsInService, String name) {
		_age = age;
		_yearsInService = yearsInService;
		_name = name;
	}//end of constructor
	
	
	//methods
	public String getName() {
		return _name;
	}//end of method getName
	
	public int getAge() {
		return _age;
	}//end of method getAge
	
	public int getYearsInService() {
		return _yearsInService;
	}//end of method getYearsInService


	@Override
	public int hashCode() {
		return Objects.hash(_name);
	}


	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (!(obj instanceof MyCrewMember))
			return false;
		MyCrewMember other = (MyCrewMember) obj;
		return Objects.equals(_name, other._name);
	}
	
	
	
}//end of abstract class MyCrewMember
