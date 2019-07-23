package com.journaldev.innerclasses;

public class MainClass {

	private String s_main_class;

	public void print() {
		String s_print_method = "";
		// local inner class inside the method
		class Logger {
			// able to access enclosing class variables
			String name = s_main_class; 
			// able to access non-final method variables
			String name1 = s_print_method; 

			public void foo() {
				String name1 = s_print_method;
				// Below code will throw compile time error:
				// Local variable s_print_method defined in an enclosing scope must be final or effectively final 
				// s_print_method= ":";
			}
		}
		// instantiate local inner class in the method to use
		Logger logger = new Logger();

	}
}
