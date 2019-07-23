package ex_java18;

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
			
			long length_l = Integer.toUnsignedLong(length);
			long type_l = Integer.toUnsignedLong(type);
			long errorCode_l = Integer.toUnsignedLong(errorCode);
			long elementsNum_l = Integer.toUnsignedLong(elementsNum);
			
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
			    
			    System.out.println("l Size/Length2: "+ length_l);
			    System.out.println("l Type:"+ type_l);
			    System.out.println("l errorCode:"+ errorCode_l);
			    System.out.println("l elementsNum:"+ elementsNum_l);
			    

			    System.out.println("U Size/Length2: "+ length_u);
			    System.out.println("U Type:"+ type_u);
			    System.out.println("U errorCode:"+ errorCode_u);
			    System.out.println("U elementsNum:"+ elementsNum_u);
			    System.out.println("U Message:"+message+"\n");
			    if (type_l == 2) {
			    	System.out.println("Type==2 :: BPL_LCU_STATE");
			    	long bandIndex, startFreq_100Hz, stopFreq_100Hz, state, stateset, ncType, dsaType, decisionConfidence;
			    	int spectrumQuality_dBofLCU, averagePower_dBmOfLCU, maximumPower_dBmOfLCU;
			    	long stdPower_dBofLCU, lcuScore;
			    	bandIndex = Integer.toUnsignedLong(inFromServer.readInt());
			    	startFreq_100Hz = Integer.toUnsignedLong(inFromServer.readInt());
			    	stopFreq_100Hz = Integer.toUnsignedLong(inFromServer.readInt());
			    	state = Integer.toUnsignedLong(inFromServer.readInt());
			    	state = Integer.toUnsignedLong(inFromServer.readInt());
			    	ncType = Integer.toUnsignedLong(inFromServer.readInt());
			    	dsaType = Integer.toUnsignedLong(inFromServer.readInt());
			    	decisionConfidence = Integer.toUnsignedLong(inFromServer.readInt());
			    	spectrumQuality_dBofLCU = inFromServer.readInt();
			    	averagePower_dBmOfLCU = inFromServer.readInt();
			    	maximumPower_dBmOfLCU = inFromServer.readInt();
			    	stdPower_dBofLCU = Integer.toUnsignedLong(inFromServer.readInt());
			    	stdPower_dBofLCU = Integer.toUnsignedLong(inFromServer.readInt());
			    	System.out.println("Values! \n");
			    }
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
	public class MsgDsaSate{
		private static final int byteSize = 4; 
		public long state;
	}
	public class MsgLcuConfig{
		private static final int byteSize = 28; 
		private static final int DSA_MAX_FREQ_BANDS = 400;
		//ByteSize * MAX BANDS = 11200
		public long bandId, bandIndex, lcuStart, lcuNum, freqStart_100Hz, freqSize_Hz, freqStep_Hz;
		
	}
	public class MsgLcuSate{
		private static final int byteSize = 56;
		private static final int MAX_LCUS_PER_BPL_MSG = 160; 
		public long bandIndex, startFreq_100Hz, stopFreq_100Hz, state, stateset, ncType, dsaType, decisionConfidence;
    	public int spectrumQuality_dBofLCU, averagePower_dBmOfLCU, maximumPower_dBmOfLCU;
    	public long stdPower_dBofLCU, lcuScore;
	}
	public class MsgConnectionRadioChannel{
		private static final int byteSize = 452; 
		public long connectionId; 		//from UINT32 to long
		
		//originally part of MessageRadioChannel_s
		//from UINT32 to long
		public long bandIndex, channelIndex, lcuIndex, channelNumber, centerFreq_100Hz, freqSize_Hz, channelFlags;  
	}
	public class MsgConnectionChannelDescriptors{
		private static final int byteSize = 324; 
		//from UINT32 to long
		public long connectionId;
		
		//originally part of BPL_MessageChannelDescriptor_s
		//types converted from USHORT to int.
		public int channelIndex, lcuIndex, bandIndex, channelType, channelState;		
	}
	public class MsgConnectionState{
		private static final int byteSize = 20; 
		public long a1, aa2;
		public int a3;
		public long a4, a5;
	}
	public class MsgGroupState{
		private static final int byteSize = 31; 
		//Originally struct NODEID_NET_ADDR, USHORT->int	
		
		//nodeId, connectionId, globalGroupId, state, topology, numberOfMembers, localMemberStrength, reportedMemberStrength,
        //reportedMasterStrength, localCommonalityIndex, reportedCommonalityIndex, numGroupsParticipatingIn, nonMembersNum, masterNodeId, masterBackupNodeId, eventNumber
		
	}
	public class ModemNetworkInfo{
		private static final int byteSize = 126; 
		//nodeType, NetAddr[MAC_ADDR_LENGTH], fpgaBuildTime, fpgaRev, rfBoardId, DspVersion, boardType, VersionInfo
	}
	public class MessageSecurityMode{
		private static final int byteSize = 4; 
		//mode
	}
	public class MessageLcuRssi{
		private static final int byteSize = 26;
		private static final int MAX_LCUS_PER_BPL_MSG = 160; 
		//ByteSize * MAX LCUS = 10400
		//lcuIdx, bandIdx, rssi_dBm, freqStart_100Hz, freqStop_100Hz, ncTypeMask, dsaTypeMask
	}
	public class SetWorkingChannel{
		private static final int byteSize = 12; 
		//channelNum, connectionId, fixedChannel
	}
	public class ManageConnection{
		private static final int byteSize = 8; 
		//action, connectionId, 
	}
	public class MessageSetTxFrequency{
		private static final int byteSize = 8; 
		//frequency_100Hz, waitForComplete, 
	}
	public class MessageSetTxRx{
		private static final int byteSize = 16;
		//bitMapTx, bitMapRx, connectionId, waitforCompletion_Debug
	}
	public class txPower_dBm{
		private static final int byteSize = 4; 
		public long txPower_dBm;
	}
	
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