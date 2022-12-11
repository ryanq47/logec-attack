# logec-attack
Welcome to Logec-Attack (LA) - A (minimal attempt at a) clone of Cobalt Strike, created to learn how offensive tools work. <br>

blah blah talk about agents/client and other features, have a section for shells, and for teh encryption & basic usage


## _How does LA work?:_

LA works off a client server model, similar to how a CS Beacon, or even a Meterpreter instance works. You input commands into the server,
and the client recieves, and runs them. Your job is to get the client onto the target machine, and let LA take care of the rest. 

## _Getting Started:_
Let's talk about what "The Rest" is:

The Main Shell:
  The "Main Shell" is the first point of contact with the target, it's very simple, on purpose. It uses Python's build in subprocess module to run commands on the target system - and from what I can tell, this is not picked up by Windows Defender at this time, as subprocess is used quite often. Where things may get hairy, is the connection back to the Server. The client tries to connect every 30 seconds (until connected) by default, and a firewall may block that. 

To Listen for a client connection, click Target -> Listen For Connection. In the popup, enter the listener details. 
>![image](https://user-images.githubusercontent.com/91687869/206892006-c2031f89-ba95-447d-a056-fafd5edcd133.png)

>Click Listen, and LA will now be listening: <br>
>![image](https://user-images.githubusercontent.com/91687869/206892035-3a962ef6-ea08-4c3a-8078-65969c6a9927.png)

> Upon connection, LA will display 'Connected' with a green background ***
>![image](https://user-images.githubusercontent.com/91687869/206892202-4a92ab41-e5ed-46db-835a-c5318190fa9a.png)

_***: Known bug, 'Connected' may not turn green, but if it says connected, you are connected_

Now let's get into the fun stuff - but fair warning, these actions are very loud, and could set off a lot of alarms

Target Info:
  The 'Target Info' button gathers some data about your target, such as their IP address, OS version, and Device HostName. This is unlikely to set off any alarms, but still be cautious. 

## _Reverse Shells:_
  Currently, there are 3 reverse shells avaible using Python, Perl, and Ruby*. Once connected via the "Main Shell", you can click Target -> Spawn Shell -> Language (Hover over language of choice) -> Linux or Windows**
 
>Selecting a shell:<br>
![image](https://user-images.githubusercontent.com/91687869/206891032-7c476ffb-4bea-4438-ae5a-74da547982cf.png)

>Shell Popup menu:<br>
![image](https://user-images.githubusercontent.com/91687869/206891820-3fbadd92-7b2f-4e80-8d4e-03f9aeb0419d.png)


At the moment, LA _cannot_ catch the shell for you, so you have to start your own listener using netcat (nc -lvnp PORT). 

* = Note, the ruby shell is not fully interactive at this time (No nano, vi, or any password prompts etc) <br>
** Explicit windows shells are coming, for now you can just enter the location of cmd.exe in the 'program' feild as a workaround

## _The Destruction Tab: <br>_
  Forewarning - The name is very fitting to all modules here for a reason, they will break, disable, and/or outright demolish a system - so be very careful. <br>
  >Encryption Menu:<br>
  'Encrypt Files': A module that will encrypt a target directory via AES encryption - you can even choose your own password. <br>
   ![image](https://user-images.githubusercontent.com/91687869/206891627-b1a39a5e-c0ec-4f60-aafb-773afe33e5b4.png)

  


Diagrams: <br>

Network Diagram: <br>
![image](https://user-images.githubusercontent.com/91687869/206885050-58326a5f-c243-4931-a7ea-725d1f92bf0f.png) <br>

Program Layout: <br>
![image](https://user-images.githubusercontent.com/91687869/206885056-85b932d1-1344-4020-8336-522bf4b36e1b.png)
