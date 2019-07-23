package pkg_top.pkg_middle.pkgBottom;
import pkg_top.topPrint;

public class ex_botttomUseTop {
	
	public static void main(String[] args) {
		System.out.println("Hello! This is from F[ex_botttomUseTop] M[main]");
		// Use a class within the same package
		
		//declare->initialize
		System.out.println("-declare and initialize class. This is in [TOP PACKAGE]");
		topPrint aObj = new topPrint();
		
		aObj.printInfo();
		System.out.println("/end main");
	}
}
