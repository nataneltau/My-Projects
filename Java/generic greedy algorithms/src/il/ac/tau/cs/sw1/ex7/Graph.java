package il.ac.tau.cs.sw1.ex7;

import java.util.*;

public class Graph implements Greedy<Graph.Edge> {
	List<Edge> lst; // Graph is represented in Edge-List. It is undirected. Assumed to be connected.
	int n; // nodes are in [0,...,n]

	Graph(int n1, List<Edge> lst1) {
		lst = lst1;
		n = n1;
	}

	public static class Edge {
		int node1, node2;
		double weight;

		Edge(int n1, int n2, double w) {
			node1 = n1;
			node2 = n2;
			weight = w;
		}

		@Override
		public String toString() {
			return "{" + "(" + node1 + "," + node2 + "), weight=" + weight + '}';
		}
	}

	@Override
	public Iterator<Edge> selection() {
		
		int [][] arr;
		
		sortAsAsked(lst);// write new sort because the sort in FKS don't work here
		
		arr = makeNeighborMatrix(lst,n);
		
		if(unconnected(arr))
			return null;
		
		return this.lst.iterator();

	}// end of method selection
	
	
	private static int[][] makeNeighborMatrix(List<Edge> lst, int n) {
		// declaration of variables
				int firstNode, secNode;
				int[][] arr = new int[n+1][n+1];


				for(int i=0; i<arr.length; i++) {
					for(int j=0; j<arr.length; j++)
						arr[i][j] =0;
					
					
				}//end of for
				/*
				 * the edge element isn't in candidates_lst yet, all we need to do is search a
				 * path from node2 to node1
				 */
				for (int i = 0; i <lst.size(); i++) {

					firstNode = lst.get(i).node1;
					secNode = lst.get(i).node2;

					arr[firstNode][secNode] = 1;
					arr[secNode][firstNode] = 1;
					
				} // end of for

		return arr;
	}//end of private method makeNeighborMatrix

	private static boolean unconnected(int[][] arr) {
		//declaration of variables
		boolean path=true;
		
		for(int i=1; i<arr.length; i++) {
			path = existPath(arr, 0, i);
			if(path==false)
				return true;
			
		}//end of for
		
		return false;
	}//end of private method unconnected
	
	private static void sortAsAsked(List<Edge> lst) {// bubble sort, cause easy sort
		// declaration of variables
		double valSrt1, valSrt2;
		Edge temp;

		for (int i = 0; i < lst.size(); i++) {

			for (int j = 0; j < lst.size() - i - 1; j++) {

				if (lst.get(j).weight == lst.get(j + 1).weight) {// same weight

					if (lst.get(j).node1 == lst.get(j + 1).node1) {// same first node
						valSrt1 = lst.get(j).node2;
						valSrt2 = lst.get(j + 1).node2;
					} // end of if

					else {// first node different
						valSrt1 = lst.get(j).node1;
						valSrt2 = lst.get(j + 1).node1;

					} // end of else

				} // end of if

				else {// weight different
					valSrt1 = lst.get(j).weight;
					valSrt2 = lst.get(j + 1).weight;

				} // end of else

				if (valSrt1 > valSrt2) {

					temp = lst.get(j);
					lst.set(j, lst.get(j + 1));
					lst.set(j + 1, temp);

				} // end of if

			} // end of inner for

		} // end of external for

	}// end of private method sortAsAsked

	@Override
	public boolean feasibility(List<Edge> candidates_lst, Edge element) {
		
		boolean therePath;
		int[][] arr;
		if(element.node1 == element.node2)//dont want loops
			return false;
		
		arr = makeNeighborMatrix(candidates_lst, n);
		therePath = existPath(arr, element.node1, element.node2);

		return !therePath;//if there is a path don't add, else add
	}// end of method feasibility

	/**
	 * this alg inspired by question 2 in assignment 3 but different cause not same question
	 * I am aware that there is a better algs (like BFS or DFS) but didn't know if i can use
	 * them
	 * @param arr = the graph
	 * @param start = the node we start the path
	 * @param dest = the node we should end the path
	 * @pre the graph is a forest && the graph represented as neighbor matrix
	 * @return true iff there is a path between start and dest
	 */
	private static boolean existPath(int[][] arr, int start, int dest) {
		
		
		if(arr[start][dest] == 1 || arr[dest][start]==1) {
			
			return true;
			
		}//end of if
		
		boolean check = false;
		
		for(int i=0; i<arr.length; i++) {
			
			if(arr[start][i] == 1) {
				
				arr[start][i] =0;
				arr[i][start]=0;
				
				check = existPath(arr, i, dest);
				
				arr[start][i] =1;
				arr[i][start]=1;
				
				if(check == true)
					return true;
				
				
			}//end of if
			
		}//end of for
		
		
		return check;
		
	}// end of private method existPath

	@Override
	public void assign(List<Edge> candidates_lst, Edge element) {
		
		candidates_lst.add(element);
		
	}

	@Override
	public boolean solution(List<Edge> candidates_lst) {
		return candidates_lst.size() == n ;
	}
}
