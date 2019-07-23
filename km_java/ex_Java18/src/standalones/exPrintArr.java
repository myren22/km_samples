package standalones;

//=============
// I am ashamed to admit how many times I have forgotten or mixed up steps of
// creation for arrays. 
//     declaration->allocate size-> initialize elements
//=============
public class exPrintArr {

	public static void main(String[] args) {
		//============ 1. Basic Step by Step version ==========
		// declares an array of integers
	    int[ ] A;

	    // allocates memory for 5 integers
	    A = new int[5];

	    // initialize elements
	    A[0] = 15;//first element

	    A[1] = 20;//second element

	    A[2] = 25;//third element

	    A[3] = 30;//fourth element

	    A[4] = 50;//fifth element
	    
	    System.out.println("Element at index 0: "   + A[0]);
		System.out.println("Element at index 1: "   + A[1]);
		System.out.println("Element at index 2: "   + A[2]);
		System.out.println("Element at index 3: "   + A[3]);
		System.out.println("Element at index 4: "   + A[4]);
		
		//============ 2. Declare & Size, then later initialize ==========
		int[] B = new int[3];
		
		// initialize elements
	    B[0] = 15;//first element

	    B[1] = 20;//second element

	    B[2] = 25;//third element
	    
	    //With SIZE set, this way of INIT will NOT work.
	    //B = {0, 1 ,2}
	    
	    //========= 3. All at once. Decl->Size->Init ==========
	    //Couple ways to perform all 3 in one statement. 
	    int[] C1 = new int[] {0,1,2,3};
	    
	    int[] C2 = {2,3,4,5,6,7,8};
	    
	    String[] myStringArray = new String[]{"a", "b", "c"};
		
	}

}
