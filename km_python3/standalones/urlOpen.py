'''
Created on Oct 10, 2018

@author: Kyle
'''
from urllib.request import urlopen

ip= '192.168.6.53'
cmdToSendIn=':ATT?'
cmdToSend = r'http://'+ip+r'/'+ cmdToSendIn
PTE_Return=''


#try:
HTTP_Result = urlopen(cmdToSend)

# if readResponse:
PTE_Return = HTTP_Result.read()
print('cmdToSend:{0}  , MC-VarAtn Response:{1}'.format(cmdToSendIn, PTE_Return.decode('ascii')))
# The switch displays a web GUI for unrecognised commands
if len(PTE_Return) > 100:
    print("Error, command not found:", cmdToSend)
    PTE_Return = "Invalid Command!"
# Catch an exception if URL is incorrect (incorrect IP or disconnected)
#===============================================================================
# except Exception as e:
#     print("Error, no response from device; check IP address and connections.")
#     PTE_Return = "No Response!"
#===============================================================================
# Return the response
