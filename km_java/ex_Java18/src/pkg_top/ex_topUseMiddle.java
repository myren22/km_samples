package pkg_top;
import pkg_top.pkg_middle.middlePrint;


//import ex_java18.pkgTop.pkgMiddle.middlePrint;  <-- Not this because none of the packages 
//												      say ex_java18 when declaring their packagename

public class ex_topUseMiddle {

	public static void main(String[] args) {
		System.out.println("Hello! This is from F[ex_topUseMiddle] M[main]");
		// Use a class within the same package
		
		//declare->initialize
		System.out.println("-declare and initialize class. This is in [MIDDLE PACKAGE]");
		middlePrint aObj = new middlePrint();
		
		aObj.printInfo();
		System.out.println("/end main");
	}
}
