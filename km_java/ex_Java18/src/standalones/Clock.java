package standalones;

public class Clock{
	//basically a struct with a couple fields. Will be used to store vals, then set vals
	public final static int byteSize = 12; //3 vars, 4 bytes each
	public int hour, minute, second;
	public String timeFormat;
	
	Clock(int hour, int minute, int second) {
		this.hour=hour;
		this.minute=minute;
		this.second=second;
	}
}