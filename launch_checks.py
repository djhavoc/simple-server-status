#### Simple Server Status
####
#### http://github.com/joet3ch/simple-server-status
####
#### joet3ch (joe@t3ch.com)
####

## launch all checks

import sys
sys.path.append('Classes/')
import Check
 
if __name__ == "__main__":
    launcher = Check.Checks()

    launcher.servicesToInspect('mysql')
    launcher.run('mysql')

    launcher.servicesToInspect('http')
    launcher.run('http')

    launcher.servicesToInspect('tcp')
    launcher.run('tcp')
