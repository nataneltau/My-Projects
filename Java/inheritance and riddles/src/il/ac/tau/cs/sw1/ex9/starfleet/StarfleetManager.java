package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.*;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Map.*;
import java.util.Set;

public class StarfleetManager {

	/**
	 * Returns a list containing string representation of all fleet ships, sorted in
	 * descending order by fire power, and then in descending order by commission
	 * year, and finally in ascending order by name
	 */
	public static List<String> getShipDescriptionsSortedByFirePowerAndCommissionYear(Collection<Spaceship> fleet) {
		//declaration of variables
		List<String> lst = new ArrayList<>();
		List<Spaceship> lstSpaceship = new ArrayList<>();

		for (Spaceship ship : fleet) {
			lstSpaceship.add(ship);
		}

		Collections.sort(lstSpaceship);

		for (Spaceship ship : lstSpaceship) {
			lst.add(ship.toString());
		}

		return lst;
	}// end of method getShipDescriptionsSortedByFirePowerAndCommissionYear

	/**
	 * Returns a map containing ship type names as keys (the class name) and the
	 * number of instances created for each type as values
	 */
	public static Map<String, Integer> getInstanceNumberPerClass(Collection<Spaceship> fleet) {
		//declaration of variables
		Map<String, Integer> map = new HashMap<>();
		String shipType;

		for (Spaceship ship : fleet) {

			shipType = ship.getClass().getSimpleName();
			addToTheMap(map, shipType);

		} // end of for

		return map;

	}// end of method getInstanceNumberPerClass

	private static void addToTheMap(Map<String, Integer> map, String className) {

		if (!(map.containsKey(className))) {
			map.put(className, 1);
		} // end of if

		else {// map.containsKey(className) == true

			int num = map.get(className) + 1;
			map.put(className, num);

		} // end of else

	}// end of private method addToTheMap

	/**
	 * Returns the total annual maintenance cost of the fleet (which is the sum of
	 * maintenance costs of all the fleet's ships)
	 */
	public static int getTotalMaintenanceCost(Collection<Spaceship> fleet) {
		int sum = 0;

		for (Spaceship ship : fleet) {
			sum += ship.getAnnualMaintenanceCost();
		} // end of for

		return sum;

	}// end of method getTotalMaintenanceCost

	/**
	 * Returns a set containing the names of all the fleet's weapons installed on
	 * any ship
	 */
	public static Set<String> getFleetWeaponNames(Collection<Spaceship> fleet) {
		//declaration of variables
		Set<String> weaponNames = new TreeSet<>();
		List<Weapon> weapons = new ArrayList<>();

		for (Spaceship ship : fleet) {

			if (ship instanceof MyBattleSpaceship) {
				weapons = ((MyBattleSpaceship) ship).getWeapon();

				for (Weapon wep : weapons) {

					weaponNames.add(wep.getName());

				} // end of inner for

			} // end of if

		} // end of for

		return weaponNames;

	}// end of method getFleetWeaponNames

	/*
	 * Returns the total number of crew-members serving on board of the given
	 * fleet's ships.
	 */
	public static int getTotalNumberOfFleetCrewMembers(Collection<Spaceship> fleet) {
		//declaration of variables
		int membersNum = 0;
		Set<? extends CrewMember> set = new HashSet<>();

		for (Spaceship ship : fleet) {

			set = ship.getCrewMembers();

			membersNum += set.size();

		} // end of for

		return membersNum;

	}// end of method getTotalNumberOfFleetCrewMembers

	/*
	 * Returns the average age of all officers serving on board of the given fleet's
	 * ships.
	 */
	public static float getAverageAgeOfFleetOfficers(Collection<Spaceship> fleet) {
		//declaration of variables
		int counter = 0;
		float ageSum = 0f;
		Set<? extends CrewMember> set = new HashSet<>();

		for (Spaceship ship : fleet) {

			set = ship.getCrewMembers();

			for (CrewMember crew : set) {

				if (crew instanceof Officer) {
					ageSum += crew.getAge();
					counter++;
				} // end of if

			} // end of inner for

		} // end of for

		return ageSum / counter;// counter!=0 because there is at least one officer at the fleet

	}// end of method getAverageAgeOfFleetOfficers

	/*
	 * Returns a map mapping the highest ranking officer on each ship (as keys), to
	 * his ship (as values).
	 */
	public static Map<Officer, Spaceship> getHighestRankingOfficerPerShip(Collection<Spaceship> fleet) {
		//declaration of variables
		Map<Officer, Spaceship> mapHighestRank = new HashMap<>();
		Set<? extends CrewMember> set = new HashSet<>();
		Officer highestRank;
		List<Officer> allOfficersInSpaceship = new ArrayList<>();

		for (Spaceship ship : fleet) {

			set = ship.getCrewMembers();
			allOfficersInSpaceship.clear();
			
			for (CrewMember crew : set) {

				if (crew instanceof Officer) {

					allOfficersInSpaceship.add((Officer) crew);

				} // end of if

			} // end of inner for

			if (allOfficersInSpaceship.size() > 0) {

				highestRank = Collections.max(allOfficersInSpaceship);

				mapHighestRank.put(highestRank, ship);

			} // end of for

		} // end of for

		return mapHighestRank;

	}// end of method getHighestRankingOfficerPerShip

	/*
	 * Returns a List of entries representing ranks and their occurrences. Each
	 * entry represents a pair composed of an officer rank, and the number of its
	 * occurrences among starfleet personnel. The returned list is sorted
	 * ascendingly based on the number of occurrences.
	 */
	public static List<Map.Entry<OfficerRank, Integer>> getOfficerRanksSortedByPopularity(Collection<Spaceship> fleet) {
		//declaration of variables
		Map<OfficerRank, Integer> mapOfTheRanks = new HashMap<>();
		Set<? extends CrewMember> set = new HashSet<>();
		List<Map.Entry<OfficerRank, Integer>> officersRankPopularity;
		int num;
		Officer officer;


		for (Spaceship ship : fleet) {

			set = ship.getCrewMembers();

			for (CrewMember crew : set) {

				if (crew instanceof Officer) {
					
					officer = (Officer)crew;
					
					if(mapOfTheRanks.containsKey(officer.getRank())) {
						
						num = mapOfTheRanks.get(officer.getRank())+1;
						mapOfTheRanks.put(officer.getRank(), num);
						
					}//end of inner if
					
					else {
						
						mapOfTheRanks.put(officer.getRank(), 1);
						
					}//end of inner else
					
				}//end of if
				
			}//end of inner for
			
		}//end of outer for
		
		officersRankPopularity = new ArrayList<>(mapOfTheRanks.entrySet());
		
		Collections.sort(officersRankPopularity, (x, y)->{
			int temp1, temp2 ,res;
			
			temp1 = x.getValue();
			temp2 = y.getValue();
			
			res = Integer.compare(temp1, temp2);
			
			if(res ==0) {
				
				res = x.getKey().compareTo(y.getKey());
				
			}//end of if 
			
			
			return res;
		});

		return officersRankPopularity;
		
		
		
		
	}// end of method getOfficerRanksSortedByPopularity
	
	
}//end of class StarfleetManager
