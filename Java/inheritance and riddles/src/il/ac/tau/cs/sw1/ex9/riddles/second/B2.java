package il.ac.tau.cs.sw1.ex9.riddles.second;

public class B2 extends A2 {
	
	
	public A2 getA(boolean rand) {
		
		if(rand == false)
			return new A2();
		
		//rand == true
		return new B2();
		
	}
	public String foo(String s) {
		return s.toUpperCase();

	}
}
