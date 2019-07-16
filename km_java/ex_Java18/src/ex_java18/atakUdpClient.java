package ex_java18;

import java.io.*;
import java.net.*;

import java.util.Timer;
import java.util.TimerTask;
import java.io.IOException;
import java.io.InterruptedIOException;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.MulticastSocket;
import java.net.DatagramSocket;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.SocketAddress;
import java.util.Properties;
import java.util.Enumeration;
import java.util.Arrays;

/**
 * Another device with this plugin would be responsible for listening for the messages.   This
 * is a sample loop that is listening for traffic, checking to see that it is from and external
 * device and processing the message.
 */

//class UDPListener implements Runnable {
//	public static final String TAG = "CommoutMapComponent";
//
//    private final int RATE = 3000;
//    private final int receiveTimeout = RATE * 3;
//
//    private final int retryTimeout = 1000;
//    private final int ttl = 12;
//
//    public Context pluginContext;
//    public MapView _mapView;
//
//    private String outputAddress = "233.1.1.1";
//    private int outputPort = 8900;
//
//    private boolean cancelled = false;
//
//    public void cancel() {
//        cancelled = true;
//    }
//
//    public boolean isCancelled() {
//        return cancelled;
//    }
//
//    @Override
//    public void run() {
//        Log.d(TAG, "starting the run");
//        DatagramSocket socket = null;
//        InetAddress address = null;
//        SocketAddress sockAddr = null;
//
//        try {
//            // create socket and set properties
//            address = InetAddress.getByName(outputAddress);
//        } catch (UnknownHostException e1) {
//            // unknown host error
//            return;
//        }
//        final byte[] message = new byte[8 * 1024];
//        final DatagramPacket p = new DatagramPacket(message,
//                message.length);
//
//        // run
//        while (!cancelled) {
//            try {
//                if (socket == null) {
//                    socket = SocketFactory.getSocketFactory()
//                            .createMulticastSocket(outputPort);
//                    socket.setSoTimeout(receiveTimeout);
//
//                    if (address.isMulticastAddress()) {
//                        ((MulticastSocket) socket).joinGroup(address);
//                    }
//                }
//
//                // receive packet
//                socket.receive(p);
//                // dumbest way to filter, remember this is a simple example
//                if (!p.getAddress().toString()
//                        .contains(NetworkUtils.getIP())) {
//                    byte[] b = p.getData();
//                    String s = new String(b);
//                    s = s.substring(0, p.getLength());
//                    toMapItem(s.getBytes());
//                    Log.d(TAG, "received: " + s);
//                } else {
//                    //byte[] b = p.getData();
//                    //String s = new String(b);
//                    //s = s.substring(0, p.getLength());
//                    //Log.d(TAG, "received loopback: " + s);
//                }
//
//            } catch (InterruptedIOException toe) {
////                Log.d(TAG, "interrupted exception occured: " + toe);
//
//                // timeout
//                socket.close();
//                socket = null;
//            } catch (IOException e1) {
////                Log.d(TAG, "ioexception occured for udp receieve: " + e1);
//
//                e1.printStackTrace();
//                // receive error
//                try {
//                    Thread.sleep(retryTimeout);
//                } catch (Exception e) {
//                }
//                socket.close();
//                socket = null;
//            } catch (Exception e2) {
////                Log.d(TAG, "exception occured for udp receive: " + e2);
//                e2.printStackTrace();
//
//                // general error
//                try {
//                    Thread.sleep(retryTimeout);
//                } catch (Exception e) {
//                }
//                socket.close();
//                socket = null;
//            }
//        }
//
//        // clean up
//        if (socket != null) {
//            try {
//                socket.close();
//            } catch (Exception e) {
//            }
//        }
//    }
//}
//
//class atakUdpClient {
//	public static void main(String argv[]) throws Exception {
//		System.out.println("TCPClient start.");
//		String sentence;
//		String modifiedSentence;
//		BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
//		System.out.println("TCPClient new inputStreamRead system.in.");
//		Socket clientSocket = new Socket("localhost", 6789);
//		DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
//		BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
//		//do things. Read User Line -> Write Bytes to Server ->  Read in From Server -> Print response from server.
//		System.out.println("TCPClient readLine now");
//		sentence = inFromUser.readLine();
//		System.out.println("TCPClient write.");
//		System.out.println("  Sent:>"+sentence);
//		outToServer.writeBytes(sentence + '\n');  //new line is required to end message
//		System.out.println("Waiting for response from server...");
//		modifiedSentence = inFromServer.readLine();
//		System.out.println("FROM SERVER: " + modifiedSentence);
//		clientSocket.close();
//	}
//}

