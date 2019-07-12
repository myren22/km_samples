package ex_Java18;

import java.io.*;
import java.net.*;

class TCPClient_v2 {
	public static void main(String argv[]) throws Exception {
		int count=0;
		System.out.println("TCPClient start.");
		String sentence;
		String modifiedSentence;
		BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("TCPClient new inputStreamRead system.in.");
		String ipNumber;
		int portNumber;
		
//		portNumber=8080;
//		ipNumber = "100.88.70.64";

//		//ATAK
//		portNumber=8082;
////		ipNumber = "10.0.0.194";
//		ipNumber = "100.92.162.193";
		
		//ATAK
//		portNumber=8082;
//		ipNumber = "192.168.42.129";
//		
//		//BackPanelInterface
		portNumber=50001;
		ipNumber = "0.0.0.0";
//		ipNumber = "192.168.42.129";
		
		
		Socket clientSocket = new Socket(ipNumber, portNumber);
		DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
		DataInputStream inFromServer = new DataInputStream(clientSocket.getInputStream());
		BufferedReader inFromServerLine = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
		
//		//do things. Read User Line -> Write Bytes to Server ->  Read in From Server -> Print response from server.
//		if(false){
//			System.out.println("TCPClient readLine now[PLEASE TYPE INTO CONSOLOLE HERE]\nMSG:");
//			sentence = inFromUser.readLine();
//		}
//		else {
//			System.out.println("TCPClient SENDING MSG \"Hello from eclipse windows server!\"\nMSG:");
//			sentence = "Hello from eclipse windows server!";
//		}
		
		
		//byte firstReadByte[]; // <-- declaration only
//		byte firstReadByte[] = new byte[4]; // <declaration and immediate instantiation with size.
		
//		inFromServer.read(firstReadByte, 0, 4);
		

		while(count<20) {
			int length = inFromServer.readInt() ;                    // read length of incoming message
			int type = inFromServer.readInt();    
			int errorCode = inFromServer.readInt();    
			int elementsNum = inFromServer.readInt();    
			
			int length_u = inFromServer.readInt()  & 0xFF;                    // read length of incoming message
			int type_u = inFromServer.readInt() & 0xFF;    
			int errorCode_u = inFromServer.readInt() & 0xFF;    
			int elementsNum_u = inFromServer.readInt() & 0xFF;    
			if(length>0) {
				System.out.println("start length parse:"+length);
			    byte[] message = new byte[length];
			    
			    inFromServer.readFully(message, 0, message.length); // read the message
			    
			    
			    System.out.println("Size/Length:  "+message.length);
			    System.out.println("Size/Length2: "+ length);
			    System.out.println("Type:"+ type);
			    System.out.println("errorCode:"+ errorCode);
			    System.out.println("elementsNum:"+ elementsNum);
			    System.out.println("Message:"+message);
			    

			    System.out.println("U Size/Length2: "+ length_u);
			    System.out.println("U Type:"+ type_u);
			    System.out.println("U errorCode:"+ errorCode_u);
			    System.out.println("U elementsNum:"+ elementsNum_u);
			    System.out.println("U Message:"+message+"\n");
			}
			
			count++;
		}
		System.out.println("exit while");
		
		int maxSize;
		int offset=0;
		int maxLength = 16384;
		byte[] byteBufArray = null;
//		maxSize = objInpStr_FromClient.read(byteBufArray, offset, maxLength);
//		
//		objInpStr_FromClient.readFully(byteBufArray);
		
		
//		System.out.println("TCPClient write.");
//		System.out.println("  Sent:>"+sentence);
//		outToServer.writeBytes(sentence + '\n');  //new line is required to end message
		System.out.println("Waiting for response from server...");
		modifiedSentence = inFromServerLine.readLine();
		System.out.println("FROM SERVER: " + modifiedSentence);
		
		while(true) {
			count++;
//			sentence = "Hello from eclipse windows server!" + count;
//			System.out.println("  Sent:>"+sentence);
//			
//			outToServer.writeBytes(sentence + '\n');  //new line is required to end message
//			System.out.println("Waiting for response from server...");
			
			modifiedSentence = inFromServerLine.readLine();
			System.out.println("FROM SERVER: " + modifiedSentence);
			
			if (count>30) {break;}
		}
		
		
		System.out.println("--end of CLIENT PROCESS--");
		clientSocket.close();
	}
	//==================================================================
//	public enum BPL_Message_t{
//	    BPL_DSA_STATE(1),BPL_LCU_CONFIG,
//	    
//	}
	public enum BPL_MessageType_e
	{
	    BPL_DSA_STATE,                //!< DSA runtime status.
	    BPL_LCU_CONFIG,                //!< LCU configuration.
	    BPL_LCU_STATE,                //!< LCU state.
	    BPL_CONN_STATE,                //!< Connection state.
	    BPL_RADIO_CHANNELS ,                //!< Channel information reported by the radio.
	    BPL_CHANNEL_LIST ,                //!< A list of channels.
	    BPL_GRP_STATE,                //!< Group state.
	    BPL_LOG_MESSAGE,                //!< Logging message.
	    BPL_LOG_SECURITY_MODE,                //!< DSA security mode

	    BPL_RADIO_DRIVER_INFO,                //!< Radio driver info

	    BPL_RSSI_INFO,               //!< RSSI and NC information (spectrum bug)

	    BPL_MAX                //!< Used to specify the number of supported messages
	}
	/*!
	 * \enum    BPL_ToDsaMessageType_e
	 *
	 * \brief    Values that represent messages sent from back panel module to DSA. 
	 */
	enum BPL_ToDsaMessageType_e
	{
	    BPL_TO_DSA_SET_LCU_STATE,            //!< Overwrites LCU state.
	    BPL_TO_DSA_SET_DISPLAY_OPTIONS,                //!< Sets display preferences.
	    BPL_TO_DSA_SET_WORKING_CHANNEL,                //!< Sets working channel.
	    BPL_TO_DSA_MANAGE_CONNECTION,                  //!< Manages connection.
	    BPL_TO_DSA_PULL_EVERYTHING,                    //!< Pulls all updates.
	    BPL_TO_DSA_GENERATE_LOG,                       //!< Pulls current log on all DSA Core components

	    BPL_TO_DSA_GET_DRIVER_INFO,                    //!< Unused
	    BPL_TO_DSA_RELOAD_DRIVER,                      //!< Unused
	    BPL_TO_DSA_GET_FROM_FILE,                      //!< Unused
	    BPL_TO_DSA_SET_TO_FILE,                        //!< Unused
	    BPL_TO_DSA_SET_RADIO_CHANNEL_SET,              //!< Unused
	    BPL_TO_DSA_SET_TX_RX,                          //!< Unused
	    BPL_TO_DSA_DEL_CONN,                           //!< Unused
	    BPL_TO_DSA_ADD_CONN,                           //!< Unused
	    BPL_TO_DSA_SET_WORK_CHANNEL,                   //!< Unused
	    BPL_TO_DSA_SHOW_LLS_TABLE,                     //!< Unused
	    BPL_TO_DSA_GET,                                //!< Unused
	    BPL_TO_DSA_APPLY,                              //!< Unused
	    BPL_TO_DSA_UPDATE_CONTROLS,                    //!< Unused
	    BPL_TO_DSA_SET_MAX_ALLOW_POWER,                //!< Unused
	    BPL_TO_DSA_SET_TX_FREQ,                        //!< Unused
	    BPL_TO_DSA_SAMPLE_SINGLE_SCAN,                 //!< Unused
	    BPL_TO_DSA_WB_SINGLE_SCAN,                     //!< Unused
	    BPL_TO_DSA_SINGLE_READ,                        //!< Unused

	    BPL_TO_DSA_MAX                                 //!< Used to specify the number of supported messages
	}
	
	public int calculateMessageSize(int datasize) {
		return 2;
		
	}
//	public void MessageDecode(Message msg) {
//		switch (msg.what) {
//        case "A"://if one type A as choice
//            System.out.println("Thepasskey");
//            break;
//        case "B":
//            System.out.println("12345");
//            break;
//        case "C":
//            System.out.println("54321");
//            break;
//        default:
//            System.out.println("error! Check your data");
//            break;
//            
//        //=========  BPL_Message_t *pBpl ==== Taken from CBackPanel.cpp
//            
//            int      lastError = NO_ERROR;
//            int      MsgProcessed = 0;
//            ULONG    i;
//
//            if (!pBpl)
//                return OS_STATUS_INVALID_PARAMETER;
//
//            if (m_pCoreProxy->getState() < CORE_STATE_RUN || MsgProcessed)
//            {
//                if (lastError)
//                    CORE_ERROR_LOG(lastError, ("Process BPL: %u", pBpl->type));
//
//                return lastError;
//            }
//
//            APP_DEBUG_LOG(("pBpl->type %i", (int)pBpl->type));
//
//        switch (pBpl->type) {
//            case    BPL_TO_DSA_SET_LCU_STATE:
//                {
//                    UCHAR buffer[sizeof(DsaMsg_t) + sizeof(LCU_RemoteCommand_t)];
//                    DsaMsg_t *pMsg = (DsaMsg_t *)buffer;
//                    LCU_RemoteCommand_t *pCmd = (LCU_RemoteCommand_t*)pMsg->Buffer;
//
//                    if (!pBpl->elementsNum)
//                        break;
//
//                    memset(buffer, 0, sizeof(buffer));
//                    pMsg->messageType = SPEC_MGR_EVENT_PROCESS_BPL_COMMAND;
//                    pMsg->size = sizeof(LCU_RemoteCommand_t);
//
//                    for (i = 0; i < pBpl->elementsNum; i++)
//                    {
////                        pCmd->bandIdx = static_cast<UINT>(pBpl->MsgData.LcuState[i].bandIndex);
////                        pCmd->lcuIdx = static_cast<UINT>(pBpl->MsgData.LcuState[i].lcuIndex);
////                        pCmd->set = static_cast<UINT>(pBpl->MsgData.LcuState[i].stateSet);
////                        pCmd->lcuState = static_cast<ULONG>(pBpl->MsgData.LcuState[i].state);
////
////                        lastError = m_pCoreProxy->sendMessageTo(DSA_WORKER_SPECTRUM, (UCHAR *)pMsg, sizeof(DsaMsg_t) + pMsg->size - PLACEHOLDER_BUFFER);
//                        if (lastError)
//                        {
//                            NOP();
//                        }
//                    }
//                }
//                break;
//
//            case    BPL_TO_DSA_SET_DISPLAY_OPTIONS:
//                CORE_TODO_LOG((0));
//                break;
//
//            case    BPL_TO_DSA_SET_WORKING_CHANNEL:
//                RADIO_BasicChannelDescriptor_t    Channel;
//
//                Channel.frequency_100Hz = m_pCoreProxy->getFreqByChannelNumber(pBpl->MsgData.SetWorkingChannel.channelNum);
//                if (Channel.frequency_100Hz == INVALID_FREQ_VALUE)
//                {
//                    CORE_ERROR_LOG(lastError, (0));
//                    break;
//                }
//
//                memset(&Channel, 0, sizeof(RADIO_BasicChannelDescriptor_t));
//                m_pCoreProxy->setWorkingChannels(&Channel, 1, pBpl->MsgData.SetWorkingChannel.connectionId);
//                break;
//
//            case    BPL_TO_DSA_MANAGE_CONNECTION:
//                lastError = OS_STATUS_INVALID_PARAMETER;
//                CORE_TODO_LOG(("Process BPL: %u", pBpl->type));
//                break;
//
//            case    BPL_TO_DSA_PULL_EVERYTHING:
//                displayEverything();
//                break;
//
//            case    BPL_TO_DSA_GENERATE_LOG:
//                generateLog();
//                break;
//
//            case    BPL_TO_DSA_GET_FROM_FILE:
//                break;
//
//            case    BPL_TO_DSA_SET_TO_FILE:
//                break;
//
//            case    BPL_TO_DSA_SET_RADIO_CHANNEL_SET:
//                break;
//
//            case    BPL_TO_DSA_SET_TX_RX:
//                break;
//
//            case    BPL_TO_DSA_DEL_CONN:
//                break;
//
//            case    BPL_TO_DSA_ADD_CONN:
//                break;
//
//            case    BPL_TO_DSA_SET_WORK_CHANNEL:
//                break;
//
//            case    BPL_TO_DSA_SET_TX_FREQ:
//                break;
//
//            case    BPL_TO_DSA_SET_MAX_ALLOW_POWER:
//                break;
//
//            case    BPL_TO_DSA_GET_DRIVER_INFO:
//                break;
//
//            case    BPL_TO_DSA_RELOAD_DRIVER:
//                break;
//
//            default:
//                lastError = OS_STATUS_INVALID_PARAMETER;
//                CORE_ERROR_LOG(lastError, ("Process BPL: %u", pBpl->type));
//                break;
//            }
//
//            if (lastError)
//            {
//                CORE_ERROR_LOG(lastError, ("Process FPL: %u", pBpl->type));
//                return lastError;
//            }
//
//            return lastError;
//	}
}