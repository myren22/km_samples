package pkg_top.pkg_middle;

import com.sharedspectrum.dsaReader.BPL_MessageType;

public enum exEnumWeekday {	//proper naming covention is just name this class/enum Weekday.
	//constants are supposed to be all caps.
	MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY;
	
	//===============
	//... there are optional extra attributes to a java enum, that explicitly define their values.
	//However there are a couple methods enum inherits you can rely on. Check the javadocs of these.
	// .valueOf()		-
	// .ordinal()		-
	// .name()			- Returns the class name, as literally declared in file.
	// .toString()		- A method meant to overridden to provide a user chosen name. or 
	// .values()		- Returns a list that can be iterated over by the user
	//==============
//	public static final String TAG = exEnumWeekday.class.getSimpleName();
	
	
}

//==== USAGE of ENUM INSTANCE as the CONDITION of a SWITCH statement. 
//An enum can be used in a switch statement, but it is a bit specific the formatting.
//Status status = Status.COMPLETED;
//switch (status) {
//        case STARTED:
//                System.out.println("Application started");
//                break;
//        case FAILED:
//                System.out.println("Application failed");
//                break;
//        case COMPLETED:
//                System.out.println("Application completed");
//                break;
//        default:
//	         throw new IllegalArgumentException("Invalid Invocation");


//==== USAGE of VALUES to get LIST 
//List<PodSchdEnumConstants> al = Arrays.asList(PodSchdEnumConstants.values());


//BPL_MessageType typeEnum =  BPL_MessageType.forInt(2);
//String s3 = typeEnum.name();		//Returns classname