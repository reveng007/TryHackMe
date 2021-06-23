#### See This room before doing Anything related to Windows...

link:[THM](https://tryhackme.com/room/windowsfundamentals1xbx)

Task2: Windows Editions
------------------------

1. What encryption can you enable on Pro (Win10) that you can't enable in Home (Win10)?

--> Bitlocker

Task3: The Desktop (GUI)
--------------------------

1. Which selection will hide/disable the Search box?

--> hidden

2. Which selection will hide/disable the Task View button?

--> show task view button

3. Besides Clock, Volume, and Network, what other icon is visible in the Notification Area?

--> action center 

Task4: The File System
------------------------

On NTFS volumes, you can set permissions that grant or deny access to files 
and folders.

The permissions are:

1. Full control
2. Modify
3. Read & Execute
4. List folder contents
5. Read
6. Write

see: [file and folder](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-2000-server/bb727008(v=technet.10))


#### How can you view the permissions for a file or folder?
S1.
> Right-click the file or folder you want to check for permissions.
S2.
> From the context menu, select `Properties`.
S3.
> Within Properties, click on the `Security` tab.
S4.
> In the `Group or user names` list, select the user, computer, or group whose permissions you want to view.


1. What is the meaning of NTFS?

--> New Technology File System


Task5: The Windows\System32 Folders
------------------------------------

1. What is the system variable for the Windows folder?

--> %windir%

Task6: User Accounts, Profiles, and Permissions
------------------------------------------------

User accounts can be one of two types on a typical local Windows system: **`Administrator`** & **`Standard User`**.

1. An `Administrator` can make changes to the **system**: 

a. add users
b. delete users
c. modify groups
d. modify settings on the system, etc. 

2. A `Standard User` can only make changes to folders/files attributed to the user & can't perform system-level changes, such as install programs.


#### Adding User to Windows10 system:

1. Settings > Accounts > Other Users > Add someone else to this PC (opens Local User and Group Management) > right click 


shortcut to open --> Local User and Group Management: **`lusrmgr.msc`**


NOTE:  A Standard User will not see this option (Add someone else to this PC)


1. What is the name of the other user account?

--> tryhackmebilly

2. What groups is this user a member of?

--> Remote Desktop Users, Users

3. What built-in account is for guest access to the computer?

--> Guest

4. What is the account status ?

--> Account is disabled


Task7: User Account Control
----------------------------


NOTE:
> Elevated privilege increases the risk of system compromise because it makes it easier for malware to infect the system. Consequently, since the user account can make changes to the system, the malware would run in the context of the logged-in user.

##### To protect the local user with `such privileges`, Microsoft introduced User 
`Account Control (UAC)`. This concept was first introduced with the short-lived Windows Vista and continued with versions of Windows that followed.


Note: `UAC (by default)` doesn't apply for the `built-in local administrator account`.

Login to `tryhackmebilly` via remmina.


1. What does UAC mean?

--> User Account Control



Task8: Settings and the Control Panel
----------------------------------------

1. In the Control Panel, change the view to Small icons. What is the last setting in the Control Panel view?

--> Windows Defender Firewall


Task9: Task Manager
---------------------

1. What is the keyboard shortcut to open Task Manager?

--> Ctrl+Shift+Esc


