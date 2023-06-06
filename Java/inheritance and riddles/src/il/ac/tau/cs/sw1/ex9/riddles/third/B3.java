package il.ac.tau.cs.sw1.ex9.riddles.third;

public class B3 extends A3 {

	public B3(String str) {
		super(str);
	}

	public void foo(String s) throws B3 {
		if (s.equals(this.s)) {
			throw new B3(s);
		}

	}
	
	@Override
	public String getMessage() {
		return s;
	}
}