package standalones;

import java.io.*;
import java.net.*;

class exTCPClient {
	public static void main(String argv[]) throws Exception {
		System.out.println("exTCPClient start.");
		String sentence;
		String modifiedSentence;
		BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("exTCPClient new inputStreamRead system.in.");
		String ipNumber;
		int portNumber;		
		
		portNumber=50002;
		ipNumber = "0.0.0.0";
		
		
		Socket clientSocket = new Socket(ipNumber, portNumber);
		DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
		BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
		
		
		//do things. Read User Line -> Write Bytes to Server ->  Read in From Server -> Print response from server.
		int scenarioCon=2;
		
		if(scenarioCon==0){
			System.out.println("exTCPClient readLine now[PLEASE TYPE INTO CONSOLOLE HERE]\nMSG:");
			sentence = inFromUser.readLine();
		}
		else if(scenarioCon==1){
			//client sends(this program), then listens for reply. loop these 2 steps.
			
			int count = 0;
			while(count<20) {
				System.out.println("exTCPClient SENDING MSG \"Hello from eclipse windows server!\"\nMSG:");
				sentence = "Hello from eclipse windows server!";
				System.out.println("exTCPClient write.");
				System.out.println("  Sent:>"+sentence);
				outToServer.writeBytes(sentence + '\n');  //new line is required to end message
				System.out.println("Waiting for response from server...");
				modifiedSentence = inFromServer.readLine();
				System.out.println("  Response:"+ modifiedSentence);
				count++;
			}			
		}
		else if(scenarioCon==2){
			//client listens to server, then sends message. loop these 2 steps.
			
			int count = 0;
			while(count<200) {
				System.out.println("Waiting for response from server...");
				modifiedSentence = inFromServer.readLine();
				System.out.println("  Response:"+ modifiedSentence);
				
				System.out.println("exTCPClient SENDING MSG \"Hello from eclipse windows server!\"\nMSG:");
				sentence = "Hello from eclipse windows server!\n";
				System.out.println("exTCPClient write.");
				System.out.println("  Sent:>"+sentence);
				outToServer.writeBytes(sentence );  //new line is required to end message
				outToServer.flush();
				count++;
			}
			
		}
		
		
//		System.out.println("exTCPClient write.");
//		System.out.println("  Sent:>"+sentence);
//		outToServer.writeBytes(sentence + '\n');  //new line is required to end message
//		System.out.println("Waiting for response from server...");
//		modifiedSentence = inFromServer.readLine();
//		System.out.println("FROM SERVER: " + modifiedSentence);
		System.out.println("--end of CLIENT PROCESS--");
		clientSocket.close();
	}
}