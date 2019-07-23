package pkg_top.pkg_middle;


public class ex_middleUseMiddle {
	public static void main(String[] args) {
		System.out.println("Hello! This is from F[ex_middleUseMiddle] M[main]");
		// Use a class within the same package
		
		//declare->initialize
		System.out.println("-declare and initialize class. This is in [SAME PACKAGE]");
		middlePrint aObj = new middlePrint();
		aObj.printInfo();
		
		//make enum variable, and set it to a value.
		exEnumWeekday aEnum;
		aEnum = exEnumWeekday.TUESDAY;
		System.out.println("enum value:"+aEnum);
		
		System.out.println("/end main");
	}
}
