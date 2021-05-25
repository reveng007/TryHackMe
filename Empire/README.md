## Powershell Empire

`Empire`, a `C2` or `Command and Control server` created by `BC-Security`, used to deploy agents onto a device and remotely run modules. Empire is a free and open-source alternative to other command and control servers like the well known `Cobalt Strike C2`. In this room, we will cover the basics of setting up a listener and stager as well as what types are available, then learn how to use an agent on a device.

### Menu Overview:

1. `Listener` - Similar to Netcat or multi/handler for receiving back stagers.
2. `Stagers` - Similar to a payload with further functionality for deploying agents.
3. `Agents` - Used to interact with agents on the device to perform "tasks".
4. `Modules` - Modules that can be used as tools or exploits.
5. `Credentials` - Reports all credentials found when using modules.
6. `Reporting` - A report of every module and command run on each agent.

### Listeners:

#### Listeners Overview:

> Listeners are used in Empire similar to how they are used in any other normal listener like Netcat and multi/handler.
> These listeners can have some very useful functionality that can help with agent management as well as concealing your traffic / evading detections. Below you can find an outline of the available listeners and their uses.

- http - This is the standard listener that utilizes HTTP to listen on a specific port.

_The next four commands use variations of `HTTP COMs` to generate a listener, which is used to conceal traffic._ **(RESEARCH ON IT!!!)** ---> **DOAMIN FRONTING??**

1. `http_com` - Uses the standard HTTP listener with an `IE COM object`.
2. `http_foreign` - Used to point to a `different Empire server`.
3. `http_hop` - Used for `creating` an `external redirector` using `PHP`.
4. `http_mapi` - Uses the standard HTTP listener with a `MAPI COM object`.

> The next five commands all use variations of built out services or have unique features that make them different from other listeners.

1. `meterpreter` -  Used to listen for Metasploit stagers.
2. `onedrive` - Utilizes OneDrive as the listening platform.
3. `redirector` - Used for creating pivots in a network.
4. `dbx` - Utilizes Dropbox as the listening platform.
5. `http_malleable` - Used alongside the malleable C2 profiles from BC-Security.

**NOTE**:
There is also the ability to create custom malleable c2 listeners that act as beacons to emulate certain threats or APTs
[BC_-Security blog](https://www.bc-security.org/post/empire-malleable-c2-profiles/)

Now see:[TryHackMe](https://tryhackme.com/room/rppsempire)

### Stagers:

#### Stagers Overview:


