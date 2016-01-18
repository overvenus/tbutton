Tbutton
---

A mini commands launcher!

## HOW-TO

### INSTALL

```
sudo apt-get update
sudo apt-get install python-appindicator
./tbutton.py & disown
```
### Configure

Configure file can be found in `~/.config/Tbutton/`, also tray icon can be changed easily.

__configure template__:
```json
{
    // tbutton settings
    "tbutton": {
        // visible on setup?
        "hide": true
    },

    // commands go here
    "commands": {
        "NetLogin": "netlogin",

        // commands group
        // group name
        "Stop": {
            // command = command % item
            "command": "killall -s STOP %s",
            "items": {
                // item name
                "vmware": "vmware-vmx"
            }
        },

        "Cont": {
            "command": "killall -s CONT %s",
            "items": {
                "vmware": "vmware-vmx"
            }
        }
    }
}
```

## Screenshot

Captured in Ubuntu 14.04LTS

![](https://raw.githubusercontent.com/overvenus/tbutton/master/art/TbuttonScr.png)


## License

Tbutton is licensed under GPL, Version 3 (the "License")

Tbutton is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License(version 3) as published by the Free Software Foundation.
