package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Set;

public class TransportShip extends MySpaceship{
	
	private static final int BASE_ANNUAL_MAINTENANCE_COST_Transport_Ship=3000;
	private static final int COST_FOR_EACH_CARGO_CAPACITY=5;
	private static final int COST_FOR_EACH_PASSENGER_CAPACITY=3;
	private int _cargoCapacity;
	private int _passengerCapacity;
	
	
	public TransportShip(String name, int commissionYear, float maximalSpeed, Set<CrewMember> crewMembers, int cargoCapacity, int passengerCapacity){
		
		super(name, commissionYear, maximalSpeed, crewMembers);
		_cargoCapacity =cargoCapacity;
		_passengerCapacity = passengerCapacity;
		
	}//end of constructor
	
	
	public int getCargoCapacity() {
		
		return _cargoCapacity;
		
	}//end of method getCargoCapacity
	
	public int getPassengerCapacity() {
		
		return _passengerCapacity;
		
	}//end of method getPassengerCapacity
	
	public int getAnnualMaintenanceCost() {
		int forCargo, forPassenger;
		
		forCargo = getCargoCapacity()*COST_FOR_EACH_CARGO_CAPACITY;
		forPassenger = getPassengerCapacity()*COST_FOR_EACH_PASSENGER_CAPACITY;
		
		return BASE_ANNUAL_MAINTENANCE_COST_Transport_Ship+forCargo+forPassenger;
		
	}
	
	@Override
	public String toString() {
		String str;
		
		str="TransportShip\n"+super.toString()+
				"\n\tCargoCapacity="+getCargoCapacity()+
				"\n\tPassengerCapacity="+getPassengerCapacity();

		
		return str;
	}//end of method toString

}//end of class TransportShip
