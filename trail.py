import multiprocessing,time
import os,psutil
from ppadb.client import Client as AdbClient
import serial
from ppadb.command.transport import Transport 
from test import ArduinoSetup 

client=AdbClient(host="127.0.0.1",port=5037) 
devices=client.devices()
print(devices)
if len(devices)== 0:
    print("No devices Connected")
    quit()
device=devices[0] 
device2=devices[0]

'''timer1=True 
wifi_connected=False 
Fatal_error_wifi_not_connected=False'''
 



def connect_to_wifi(stateCondition):  
    stateCond={ 
        "Connection" : object,
        "Timer1" : stateCondition["Timer1"],
        "wifi_connected":stateCondition["wifi_connected"],
        "Fatal_error_wifi_not_connected":stateCondition["Fatal_error_wifi_not_connected"],
        "action1":stateCondition["action1"],
        "action2":stateCondition["action2"],
        
    }
    global device 
    device.shell("wpa_cli\n",[stateCond],handler=wifi_connect)
    
    if bool(stateCondition["wifi_connected"].value):
        print("pros2 termianted")
        return None

def run_logcat(stateCondition): 
    stateCond={ 
        "Connection" : object,
        "Timer1" : stateCondition["Timer1"],
        "wifi_connected":stateCondition["wifi_connected"],
        "Fatal_error_wifi_not_connected":stateCondition["Fatal_error_wifi_not_connected"],
        "action1":stateCondition["action1"],
        "action2":stateCondition["action2"],
        
    }
    print("running logcat")
    global device
    device.shell("logcat \n",[stateCond],handler=Check_for_unified_reason_code)

def toggleWifi(stateCondition):
    global device
    print("Disabling wifi")
    device.shell("svc wifi disable\n",{})  
    time.sleep(2)
    device.shell("svc wifi enable\n",{})
    print("Enabling Wifi")

    time.sleep(3)
    device.shell("wpa_cli\n",stateCondition,handler=check_wifi_status)  
    
    
def check_wifi_status(args):
    start=time.time() 
    print("Starting Timer from wifi status method")
    '''global Timer1
    global wifi_connected 
    global Fatal_error_wifi_not_connected''' 
    connection=args[0]["Connection"] 
    Timer1=args[0]["Timer1"] 
    Fatal_error_wifi_not_connected=args[0]["Fatal_error_wifi_not_connected"]
    wifi_connected=args[0]["wifi_connected"] 
    while True:
        command='status\n'.encode('utf-8')
        connection.write(command)
        data=connection.read(1024)
        logs=data.decode('utf-8')
        if(logs.find("wpa_state")>-1):
            if(logs.find("COMPLETED")>-1):  
                print(logs)
                print("Connected to Wifi") 
                wifi_connected.value=1
                break 
        if((time.time()-start)>60):
            Timer1.value=0   
            print("setting fatal error")
            Fatal_error_wifi_not_connected.value=1
            break
    print(wifi_connected.value)
    connection.close()
                
    
    
def wifi_connect(args): 
    connected_to_wifi =False 
    connection=args[0]["Connection"] 
    Timer1=args[0]["Timer1"] 
    Fatal_error_wifi_not_connected=args[0]["Fatal_error_wifi_not_connected"]
    wifi_connected=args[0]["wifi_connected"] 
    
    print("Running Wifi Connect Method")
    
    
    while True: 
        print("Checking Status")
        command='status\n'.encode('utf-8')
        connection.write(command)
        data=connection.read(1024)
        logs=data.decode('utf-8') 
        print(logs)
        if(logs.find("wpa_state")>-1):
            if(logs.find("COMPLETED")>-1):  
                print(logs)
                connected_to_wifi=True
                print("wifi connection already established") 
                break
            if(logs.find("SCANNING")>-1):
                time.sleep(5)
                break
            if(logs.find("DISCONNECTED")>-1):
                break
    if connected_to_wifi:
        connection.close() 
        toggleWifi(args)
        return None
    print("performing connection method")
    command='ifname=wlan0 remove_n all\n'.encode('utf-8')
    connection.write(command)
    time.sleep(1)
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)

    command='ifname=wlan0 save_config\n'.encode('utf-8')
    connection.write(command)
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs) 

    command='ifname=wlan0 ap_scan 1\n'.encode('utf-8')
    connection.write(command)
    
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)

    command='ifname=wlan0 add_n 0\n'.encode('utf-8')
    connection.write(command)
    
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)
    

    command='ifname=wlan0 set_n 0 ssid "wifi5G"\n'.encode('utf-8')
    connection.write(command)
    
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)
    command='ifname=wlan0 set_n 0 key_mgmt WPA-PSK\n'.encode('utf-8')
    connection.write(command)
    
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)
    command='ifname=wlan0 set_n 0 psk "bharath1234"\n'.encode('utf-8')
    connection.write(command)
    
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)
    command='ifname=wlan0 set_n 0 proto RSN\n'.encode('utf-8')
    connection.write(command)
    
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)
    command='ifname=wlan0 set_n 0 pairwise CCMP\n'.encode('utf-8')
    connection.write(command) 
   
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)
    command='ifname=wlan0 set_n 0 group CCMP\n'.encode('utf-8')
    connection.write(command)
   
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)
    command='ifname=wlan0 save_config\n'.encode('utf-8')
    connection.write(command)
    data=connection.read(1024)
    logs=data.decode('utf-8') 
    print(logs)
    
    
    command='ifname=wlan0 select_n 0\n'.encode('utf-8')
    connection.write(command)
    time.sleep(1)
    data=connection.read(1024) 
    logs=data.decode('utf-8') 
    print(logs)
    start=time.time() 
    print("Starting Timer from wifi status method")
    while True:
        command='ifname=wlan0 status\n'.encode('utf-8')
        connection.write(command)
        data=connection.read(1024)
        logs=data.decode('utf-8')
        if(logs.find("wpa_state")>-1):
            if(logs.find("DISCONNECTED")>-1):  
                print(logs)
                print("wifi connected and DeAuth Error") 
                wifi_connected.value=0
                Fatal_error_wifi_not_connected.value=1 
                break
        
            if(logs.find("COMPLETED")>-1):  
                print(logs)
                print("Connected to Wifi") 
                time.sleep(3) 
                if bool(wifi_connected.value):
                    break
                wifi_connected.value=1   
            if((time.time()-start)>10):
                Timer1.value=0 
                if wifi_connected.value == 1: 
                     print("wifi connected and DeAuth Error")
                else:
                    print("Automatic ConnectionFailed try connecting manually") 
                Fatal_error_wifi_not_connected.value=1
                break
                
    connection.close()
    return None
    
def Check_for_unified_reason_code(args): 
    connection=args[0]["Connection"]
    Timer1=args[0]["Timer1"] 
    Fatal_error_wifi_not_connected=args[0]["Fatal_error_wifi_not_connected"]
    wifi_connected=args[0]["wifi_connected"] 
    action1=args[0]["action1"]
    print("logact Running")
    #ser = serial.Serial('COM4', 9600, timeout=.1) 
    time.sleep(1)
    sers=ArduinoSetup() 
    ser=sers.connect()
    
    code1 = False
    timerSet = False 
    '''
    code2 = False
    code3 = False
    code4 = False
    code5 = False
    code6 = False'''
    code7 = False  
    
    
    
    
    while True:
        #global wifi_connected
        if bool(Fatal_error_wifi_not_connected.value):
            print(261)
            print("Fatal error:Wifi connection Failed exiting code")
            break 
        
        data=connection.read(1024) 
        if not data:
            break
        if data:
            logs=data.decode('utf-8')
        if(logs.find('unified network event reason')>-1):
            pos=logs.index('unified network event reason:')+30 
            reason_code=logs[pos]  
            
            if bool(Timer1.value):
                if(reason_code=="1"):
                    print("Good Connection Code "+ reason_code +" Verified")
                    code1=True 
                if(reason_code=="7"):
                    print("Good Connection Code "+ reason_code +" Verified")
                    code7=True
                if code1 and code7 :
                    print("Turning Off Router")
                    #operation_command="1"
                    #ser.write(operation_command.encode()) 
                    
            
            if(reason_code=="3"):
                print("Short disconnect Code "+ reason_code +" Verified")
            if(reason_code=="4"):
                print("Long disconnect Code "+ reason_code +" Verified")
                print("Turning Off Internet")
                #operation_command="2"
                #ser.write(operation_command.encode()) 
                #data=ser.readline()
            if(reason_code=="6"):
                print("Long unreachable Code "+ reason_code +" Verified") 
        elif (not bool(Timer1.value)): 
            if not bool(action1.value): 
                action1.value=1
                if not code1:
                    print("Good Connection Code 1  Failed")
                if not code7:
                    print("Good Connection Code  7  Failed") 
                print("Turning Off Router")
                operation_command="1"
                ser.write(operation_command.encode())  
               
        if bool(wifi_connected.value) and bool(Timer1.value):
            if not timerSet:
                timerSet=True
                start=time.time()
                print("Setting timer from Logcat",start)
            if ((time.time()-start)>20):  
                print("reason code wait time exceed ")
                Timer1.value=0
    connection.close()
    print("exiting logcat")

if __name__ == "__main__":
    
    Timer1 = multiprocessing.Value('i',1) 
    wifi_connected=multiprocessing.Value('i',0) 
    Fatal_error_wifi_not_connected=multiprocessing.Value('i',0)
    action1=multiprocessing.Value('i',0) # Turn Off Router
    action2=multiprocessing.Value('i',0) # Turn off Internet


    stateCondition={
        "Connection" : object,
        "Timer1" : Timer1,
        "wifi_connected":wifi_connected,
        "Fatal_error_wifi_not_connected":Fatal_error_wifi_not_connected,
        "action1":action1,
        "action2":action2,
        
    } 
    
    #print(type(ser))

    #run_logcat(stateCondition)

    Process1=multiprocessing.Process(target=run_logcat,args=[stateCondition,])
    Process2=multiprocessing.Process(target=connect_to_wifi,args=[stateCondition,])
#device=client.device("G0W1AQ039513006E")
    Process1.start()
    Process2.start()

    while True:
        if bool(wifi_connected.value):
            print("process2 termianted")
            Process2.kill()
            break

    Process2.join()
    Process1.join()
    
'''def shell(self, cmd,args, handler=None, timeout=None):
        conn = self.create_connection(timeout=timeout) 

        cmd = "shell:{}".format(cmd)
        conn.send(cmd)

        if handler: 
           
            args[0]['Connection']=conn
            
            handler(args)
        else:
            result = conn.read_all()
            conn.close()
            return result.decode('utf-8')'''
