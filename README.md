<h1 align="center"> EasyBot External </h1>


# Description
This is my own project, which I did about 2 years ( with breaks ).

My goal was to make this bot work on every OTS, what I was able to achieve.

The bot works externally, and its behavior is not completely predicted. There are randomized times, values, behaviors, etc..

It is possible to operate on a minimized window. We can do different things in between and it doesn't interfere with bot.

We can use the bot on multiple clients at once, and we don't have to worry about CPU or RAM consumption, as it is small.

The bot works by reading the RAM addresses of a process and based on the current state of the game image.

I leave the bot open source, I consider the project finished, most of it works, and if not you can boldly change it !

If you liked it or learned something from this project, please leave a star :star:

# Table of contents
- [Needed Libs to Run](#Needed-Python-and-Libs-to-Run)
- [Features Status](#Features-Status)
- [Currently Works On](#Currently-Works-On)
- [How To Use](#How-To-Use)
- [Video Tutorial](#Video-Tutorial)
- [How To Add New OT Client](#How-To-Add-New-OT-Client)
- [How To Make Executable](#How-To-Make-Executable)
# Needed Python and Libs to Run

- [![Python 3.10.0](https://img.shields.io/badge/python-3.10.0-blue.svg)](https://www.python.org/downloads/release/python-3100/)

- ```bash
  python -m pip install -r requirements.txt
  ```

# Features Status
- [Auto Healing](#Auto-Healing-Module) : :heavy_check_mark:
- [Cave Bot](#Cave-Bot-Module) : :heavy_check_mark:
- [Target Bot](#Target-Bot-Module) : :heavy_check_mark:
- [Auto Loot](#Auto-Loot-Module) : :heavy_check_mark:
- [Spell Attacker](#Spell-Attacker-Module) : :heavy_check_mark:
- [Lure Monsters](#Lure-Monsters-Module) : :heavy_check_mark:
- [Auto Training](#Auto-Training-Module) : :heavy_check_mark:
- [Smart Hotkeys](#Smart-Hotkeys-Module) : :heavy_check_mark:
- [Skin Monsters](#Skin-Monsters-Module) : :heavy_check_mark:
- [Record Waypoints](#Record-Waypoints-Module) : :heavy_check_mark:
- [Randomized Values](#Randomized-Values-Module) : :heavy_check_mark:
- [Stay Diagonal](#Stay-Diagonal-Module) : :heavy_check_mark:
- [Chase Target](#Chase-Target-Module) : :heavy_check_mark:
- [AI ChatBot](#AI-ChatBot-Module) : :grey_question: Soon
- [7.4 Friendly](#7.4-Friendly-Module) : :heart:
- [Timed Spells](#Timed-Spells-Module) : :heavy_check_mark:
- [Save Config](#Save-Config-Module) : :heavy_check_mark:
- [Load Config](#Load-Config-Module) : :heavy_check_mark:
- [Sort Loot](#Sort-Loot-Module) : :heavy_check_mark:
- [Multiple Bots](#Multiple-Bots-Module) : :heavy_check_mark:
- [Labels](#Labels-Module) : :grey_question: Soon
- [Actions](#Actionst-Module) : :grey_question: Soon

# Currently Works On
- [Medivia](#Medivia) : :heavy_check_mark:
- [TibiaScape](#TibiaScape) : :heavy_check_mark:
- [Miracle_DX](#Miracle) : :heavy_check_mark:
- [Treasura_DX](#Treasura) : :heavy_check_mark:
- [Dura_DX](#Dura) : :heavy_check_mark:
- [Giveria](#Giveria) : :heavy_check_mark:
- [Tibiara DX](#Tibiara) : :heavy_check_mark:
- [Igla OTS](#IglaOTS) : :heavy_check_mark:
  
# How To Use
![image](https://github.com/user-attachments/assets/12f0048b-8bbe-4cd7-ab82-d3c6831974ce)

# Settings Panel

![image](https://github.com/user-attachments/assets/94e4e247-15ea-4738-9c6a-b5f5e6b82fec)


![Blue](https://img.shields.io/badge/Set%20Character-3f48cc)  
![NoColor](https://img.shields.io/badge/You%20need%20to%20set%20middle%20of%20your%20character.-grey)  

![Red](https://img.shields.io/badge/Set%20Loot-ed1d25)  
![NoColor](https://img.shields.io/badge/You%20need%20to%20set%20the%20area%20where%20open%20bodies%20will%20appear.-grey)  

![Purple](https://img.shields.io/badge/Set%20Battle-a348a5)  
![NoColor](https://img.shields.io/badge/If%20your%20OT%20do%20not%20have%20attack%20on%20key%20set%20first%20monster%20on%20battle%20list.-grey)  

![DarkRed](https://img.shields.io/badge/Backpacks-890115)  
![NoColor](https://img.shields.io/badge/Backpack%20Info-You%20need%20to%20choose%20backpack%20coordinates%20(needed%20for%20collecting).%20If%20you%20choose%20the%20last%20field%20of%20the%20backpack,%20then%20when%20the%20backpack%20is%20filled,%20the%20next%20backpack%20inside%20will%20be%20opened.-grey)  

![Green](https://img.shields.io/badge/Runes-23b14d)  
![NoColor](https://img.shields.io/badge/You%20Need%20to%20set%20the%20coordinates%20of%20selected%20rune.-grey)  

![Grey](https://img.shields.io/badge/Tools-grey)  
![NoColor](https://img.shields.io/badge/You%20Need%20to%20set%20the%20coordinates%20of%20selected%20tool.-grey)  

# Targeting and Looting Tab

![image](https://github.com/user-attachments/assets/7c3dbda5-9bf1-4f61-b41b-cb3b80203aa8)

![Red](https://img.shields.io/badge/Targeting-ed1d25)  
![NoColor](https://img.shields.io/badge/Enter%20the%20name%20of%20the%20target,%20select%20from%20what%20distance%20to%20attack%20it,%20select%20stance%20and%20choose%20whether%20to%20skin%20it.%20Attack%20Key%20is%20the%20button%20for%20which%20it%20is%20attacking%20the%20target%20in%20the%20game.-grey)  

![Blue](https://img.shields.io/badge/Looting-3f48cc)  
![NoColor](https://img.shields.io/badge/In%20the%20first%20Text%20Box%20you%20enter%20the%20name%20of%20the%20item%20to%20collect,%20in%20the%20second%20you%20enter%20where%20this%20item%20should%20be%20droped.-grey)

![NoColor](https://img.shields.io/badge/%22--2%22%20-%20clicks%20twice%20with%20the%20left%20on%20the%20item-grey)  
![NoColor](https://img.shields.io/badge/%22--1%22%20-%20clicks%20once%20with%20the%20right%20on%20the%20item-grey)  
![NoColor](https://img.shields.io/badge/%220%22%20-%20Throws%20under%20yourself-grey)  
![NoColor](https://img.shields.io/badge/%221%22%20-%20collects%20into%20the%20first%20backpack-grey)  
![NoColor](https://img.shields.io/badge/%222%22%20-%20collects%20into%20the%20second%20backpack-grey)  
![NoColor](https://img.shields.io/badge/%223%22%20-%20collects%20into%20the%20third%20backpack-grey)  
![NoColor](https://img.shields.io/badge/%224%22%20-%20collects%20into%20the%20fourth%20backpack-grey)  

![NoColor](https://img.shields.io/badge/If%20you%20enter%20an%20item%20name%20with%20*%20at%20the%20beginning,%20e.g.%20%22*Pick%22,%20this%20image%20will%20be%20taken%20from%20local%20Images/ClientName/Sword.png%20files-grey)


![NoColor](https://img.shields.io/badge/The%20collection%20process%20is%20performed%20with%20priority.%20Items%20at%20the%20top%20of%20the%20list%20are%20collected%20first-grey)  
![NoColor](https://img.shields.io/badge/So%20if%20you%20want%20it%20to%20collect%20all%20items%20first%20and%20possibly%20open%20a%20backpack%20that%20may%20be%20in%20a%20monster%20at%20the%20end%20then%20add%20that%20backpack%20at%20the%20end%20of%20the%20list.-grey) 

![NoColor](https://img.shields.io/badge/Remember!!%20For%20looting%20to%20work%20you%20must%20have%20Background.png%2032x32%20added%20in%20Images/ClientName-grey)

![image](https://github.com/user-attachments/assets/64ab23ed-095d-4c55-8c44-6320ea1e3798)


# Smart Hotkeys

![image](https://github.com/user-attachments/assets/c5da24f9-7a0f-49e2-bee4-cefa789da302)

![Blue](https://img.shields.io/badge/Smart%20Hotkeys-3f48cc)  
![NoColor](https://img.shields.io/badge/If%20your%20server%20is%207.4%20or%20do%20not%20have%20hotkeys.%20Smart%20Hotkeys%20is%20cool%20tool%20to%20use%20hotkeys%20even%20if%20they%20are%20not%20in%20the%20game.-grey)

![NoColor](https://img.shields.io/badge/Just%20set%20the%20coordinates%20of%20rune%20that%20you%20want%20to%20use%20and%20select%20the%20hotkey%20you%20want%20it%20to%20work%20on.-grey)


# Walker

![image](https://github.com/user-attachments/assets/cb706149-21f6-40f3-8647-8ec77082ff6f)

![NoColor](https://img.shields.io/badge/Label%20and%20Action%20buttons%20do%20not%20work%20-grey)

![image](https://github.com/user-attachments/assets/200645e1-8901-4879-ae0c-e090b57dc476)

![Blue](https://img.shields.io/badge/Directions-3f48cc)  
![NoColor](https://img.shields.io/badge/Auto%20Recording%20tends%20to%20work,%20but%20to%20be%20safe%20when%20you%20use%20stairs%20I%20recommend%20turning%20it%20off%20and%20adding%20stairs%20manually.%20How%20to%20do%20that%3F-grey)

![NoColor](https://img.shields.io/badge/How%20to%20add%20stairs:-3f48cc)

![NoColor](https://img.shields.io/badge/1.%20Stand%20before%20the%20stairs%20and%20add%20waypoint%20in%20direction%20"Center"-grey)  

![NoColor](https://img.shields.io/badge/2.%20Climb%20up%20or%20down%20the%20stairs-grey)  

![NoColor](https://img.shields.io/badge/3.%20Add%20waypoint%20in%20the%20appropriate%20direction.%20Example:%20If%20north,%20then%20%22North%22%20and%20add.-grey)

# Video Tutorial
[Qucik Tutorial/Teaser on YouTube](https://www.youtube.com/watch?v=iZsd0Sz7pzA)


# How To Add New OT Client
[How To Add New OT Client](https://www.youtube.com/watch?v=dZbNfMYsa20&t=48s)

# How To Make Executable
If you want to make this bot executable version write this command in the console of the project.
```bash
pyinstaller --onefile --noconsole StartBot.py --name="EasyBot" --icon="Images/Icon.jpg"
  ```


