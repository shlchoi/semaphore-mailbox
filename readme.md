# Semaphore - Mailbox

Semaphore is a system that monitors physical mailboxes for deliveries and notifies users when mail arrives. In addition, Semaphore also categorizes and counts the number of items that are currently inside the mailbox and displays the information to the user in an associated smartphone application.  

This repository contains the code for the Mailbox Device.

Semaphore was created for the Electrical and Computer Engineering Capstone Design Symposium 2017 at the University of Waterloo.


## About Semaphore
See the [main project page](https://shlchoi.github.io/semaphore) for more information.

### Other Semaphore Repositories
* [Web Server](https://github.com/shlchoi/semaphore-server)
* [Image Processing Algorithm](https://github.com/mattcwc/semaphore-algorithm)
* [Android Application](https://github.com/shlchoi/semaphore-android)
* [iOS Application](https://github.com/shlchoi/semaphore-ios)


## Hardware
Coming soon


## Configuration
1. Add a file called `config` to the root folder
2. In `config`, add the following information:
```
{
    "mailbox_id": [ID of the mailbox],
    "server_url": [URL to the server],
    "server_port": [port the server is listening to]
}
```


## Authors

* Samson Choi 	[Github](https://github.com/shlchoi)
* Matthew Chum 	[Github](https://github.com/mattcwc)
* Lawrence Choi	[Github](https://github.com/l2choi)
* Matthew Leung [Github](https://github.com/mshleung)


## Acknowledgments
* [Ben Nuttal](https://github.com/bennuttall), [Dave Jones](https://github.com/waveform80) - [gpiozero](https://gpiozero.readthedocs.io/en/stable/)
* Raspberry Pi Foundation - [picamera](https://picamera.readthedocs.io/en/latest/)
* [Georges Toth](https://github.com/sim0nx/tsl2561) - [tsl2561](https://pypi.python.org/pypi/tsl2561)


## License

Distributed under the GNU GPLv3 license. See [LICENSE](https://github.com/shlchoi/semaphore-android/blob/master/LICENSE) for more information.

Libraries are used under the [BSD License](https://opensource.org/licenses/BSD-3-Clause).
