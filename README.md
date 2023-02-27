# windsonic

## Setup
The windsonic 2d anenometer is connected through a serial to usb converter to my linux machine. For the usb port, we first find out 
where the device is connected. To do that, we first look up all the devices connected through USB

```bash
lsusb
```
![image](https://user-images.githubusercontent.com/5336184/221494052-d58688fa-97b8-426b-8229-14739592b6af.png)

Now, we need to find out where our device PL2303 is connected. To find out, we can do the following

```bash
dmesg | grep tty
```

![image](https://user-images.githubusercontent.com/5336184/221494456-400d8cac-2177-4d2f-a3e1-5c6884f599f6.png)

To get the data, we can listen to **/dev/ttyUSB0**. On some machines, we need to change the owner on `/dev/ttyUSB0` to avoid using super user.

## Testing

For testing, we need to first setup a docker container. To setup a docker container, I used the step described 
for [virtual waggle](https://github.com/waggle-sensor/node-platforms/blob/main/vm/README.md).

To ease the setup, I have added a Makefile which simplifies the usage. The steps to setup and test the plugin are:

### Build the container

```bash
make build
```

### To deploy the container in background

```bash
make deploy
```

### To test the plugin

```bash
make interactive
```

If everything goes correctly, we should be able to test the plugin.

![image](https://user-images.githubusercontent.com/5336184/221493284-7fded052-e882-4929-981c-0211efab1ed7.png)

Note, we needed to expose **/dev/ttyUSB0** to docker container to read the data inside the docker container.
