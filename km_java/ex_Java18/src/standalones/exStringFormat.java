package standalones;

import java.util.*; 			// 1-9.
import java.util.Formatter;  	// 10. Precision formatter
public class exStringFormat {

	public static void main(String[] args) {
		//=============================================
		// 1. Space format specifier
		// 2. + Sign specifier
		// 3. ( specifier				- negatives go in parentheses
		// 4. , commaa specifier		- add commas
		// 5. - left justification specifier
		// 6. %n format specifiers		- newline
		// 7. %% format specifiers		- escape character
		// 8. %x %X format specifiers	- hexadecimal
		// 9. %e %E format specifiers	- scientific notation
		// 10. Precision Formatter Example
		//=============================================
		// General syntax format of specifier:
		//		% [flags] [width] [.precision] [argsize] typechar
		//=============================================
		// Link: https://www.geeksforgeeks.org/format-specifiers-in-java/
		
		// %s - string
		// %d - decimal integer
		// %f - float
		
		//=============================================
		// 10. Precision Formatter Example
		//=============================================
		// Create the Formatter instance 
        Formatter formatter = new Formatter(); 
  
        // added floating-point data 
        // using the %f or %e specifiers, 
        // Format to 2 decimal places 
        // in a 16 character field. 
        formatter = new Formatter(); 
        formatter.format("%16.2e", 123.1234567); 
        System.out.println("Scientific notation to 2 places: "
                           + formatter); 
  
        // Format 4 decimal places. 
        formatter = new Formatter(); 
        formatter.format("%.4f", 123.1234567); 
        System.out.println("Decimal floating-point"
                           + " notation to 4 places: "
                           + formatter); 
  
        // Format 4 places. 
        // The %g format specifier causes Formatter 
        // to use either %f or %e, whichever is shorter 
        formatter = new Formatter(); 
        formatter.format("%.4g", 123.1234567); 
        System.out.println("Scientific or Decimal floating-point "
                           + "notation to 4 places: "
                           + formatter); 
  
        // Display at most 15 characters in a string. 
        formatter = new Formatter(); 
        formatter.format("%.15s", "12345678901234567890"); 
        System.out.println("String notation to 15 places: "
                           + formatter); 
  
        // Format into 10 digit 
        formatter = new Formatter(); 
        formatter.format("%010d", 88); 
        System.out.println("value in 10 digits: "
                           + formatter); 
	}

}
