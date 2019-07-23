package pkg_top;
//==================================
//==== **** Purpose of this example ****
//==== Show that java can find other programs within the same package without any imports
//==================================

public class ex_topUseTop {

	public static void main(String[] args) {
		System.out.println("Hello! This is from F[ex_topUseTop] M[main]");
		// Use a class within the same package
		
		//declare->initialize
		System.out.println("-declare and initialize class. This is in [SAME PACKAGE]");
		topPrint aObj = new topPrint();
		
		aObj.printInfo();
		System.out.println("/end main");
	}

}
