package ex_Java18_Server;

import java.io.*;
import java.net.*;

public class TCPServer {

	public static void main(String[] args) throws Exception{
		System.out.println("TCPServer start.");
		String clientSentence;
		String capitalizedSentence;
		ServerSocket welcomeSocket = new ServerSocket(8081);
		
		System.out.println("TCPServer - now accepting...");
		Socket connectionSocket = welcomeSocket.accept();
		
		while (true) {
			
			System.out.println("TCPServer - acceped!");
			BufferedReader inFromClient  = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
			DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());
			System.out.println("TCPServer - readLine now - waiting for CLIENT send message...");
			
			//==== Read from client, change then send. Close once sent.
//			clientSentence = inFromClient.readLine();
//			System.out.println("Received: " + clientSentence);
//			capitalizedSentence = clientSentence.toUpperCase() + '\n'; //new line is required to end message.
//			outToClient.writeBytes(capitalizedSentence);
//			connectionSocket.close();
			
			//==== Send to client 1 message, then close.
			clientSentence = "Hello from Eclipse TCP Server!";
			System.out.println("Sending: " + clientSentence);
//			capitalizedSentence = clientSentence.toUpperCase() + '\n'; //new line is required to end message.
			outToClient.writeBytes(clientSentence);
			break;
		}
		connectionSocket.close();
	}
}
