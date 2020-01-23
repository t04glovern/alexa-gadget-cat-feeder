# Alexa Gadget - Cat Feeder

When [Amazon Alexa](https://alexa.amazon.com) launched in 2014 as the first major home assistant platform I was captivated by the opportunities it offered someone like me. Clearly I wasn't alone either as over the coming years we saw a boom of new generation eletronics incorportating virtual assistants in their sales pitch.

Now having voice assistant support is almost a must when launching any kind of home appliance, however this consumer demand is beginning to force hardware manufacurers to operate in a space that is very new and full of bad actors. Not all companies are technology first, so when their teams are asked to equip their white goods with internet capabilities there is a lot of room for error.

This is why I believe Amazon Alexa Gadgets are a really big deal.

---

## What is a Gadget

---

To understand the difference between an Amazon Alexa supported device, and an Alexa Gadget, you should first understand how most companies would approach building a smart assistant enabled device currently

![Alexa Smart Assistant](img/alexa-skill.png)

The architecture above is what you would usually see if the goal was to simply incorporate home assistant functionality.

1. Device registered, associated with a user. Stored in DynamoDB.
2. Call made to Alexa skill service.
3. Skill calls out to Lambda providing a unique identifier to lookup what device should have what actions performed.
4. Device is controlled over MQTT.

The problem with this architecture is it relies on understanding a number of (potentially very new) services to tie everything together. While there is nothing inheritely wrong with the design, it leaves room for error.

Alexa Gadgets on the otherhand are meant as simple companions to exist Alexa devices.

![Alexa Smart Assistant Gadget architecture](img/alexa-gadget.png)

If the goal for your product is to simply give it Alexa support then the design above is both simplier and less prone to security holes.

1. Device is paired with Echo (or any other Alexa bluetooth device).
2. Device recieves events over Bluetooth messages when skills are invoked.
3. Device can react & respond through the Alexa device.

---

## Building a Gadget

---

So you want to learn how to build a gadget? Well hopefully I can help demystifiy the process for you while we build something fun! We will be building an Alexa controlled cat feeder that is going to be controlled entirely through the Alexa Gadget interface.

### Content

---

* Alexa Gadget **Product Creation**
* Alexa Gadget **Device Setup & Registration**
* **Gadget Code** Overview
* Cat Feeder **Gadget Code**
* Cat Feeder **Alexa Skill Deployment**
* **Electronics Setup** [Optional]

### Requirements

---

* **Raspberry Pi 3 B+**: or another bluetooth microcontroller.
* **AWS Account**: [Create one if you need one](https://console.aws.amazon.com/console/home).
* **Amazon Developer account**: [create one here](https://developer.amazon.com/alexa) if you haven't already got one.
* *Optional*:
  * **3-wire servo**: To control cat feeder opening.
  * **RGB LED**: display status when skill is in use.
  * **Assortment of wires**: to wire!

**NOTE**: *While you might need to follow all steps to get a working cat feeder, they aren't necessary if you just want to learn. You can still setup a gadget (in our case a Raspberry Pi) to recieve events from Alexa!*

---

### Alexa Gadget Product Creation

---

To start with we will need to create a new Alexa Voice Service Gadget by heading over to the [products portal](https://developer.amazon.com/alexa/console/avs/products). Click **Create Product** to begin.

![Alexa Voice Service create product portal](img/avs-create-gadget-01.png)

Next you will be prompted to fill out a bunch of details about your new product. In our case we use the following details, however for your scenario feel free to change it up.

***NOTE**: The important piece of info is you MUST select Alexa Gadget as the product type.*

* **Product Name**: DevOpStar Cat Feeder
* **Product ID**: devopstar-cat-feeder
* **Product Type**: Alexa Gadget
* **Product Category**: Novelty Device
* **Product Description**: Smart Home cat feeder that will refill food bowls on request.

![Alexa Voice Service create cat feeder product](img/avs-create-gadget-02.png)

Once created, select your new product and take down the following information from the top:

* **Amazon ID**: A30XXXXXXXXXXX
* **Alexa Gadget Secret**: 4B4DXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

![Alexa Voice Service cat feeder secret details](img/avs-create-gadget-03.png)

Keep this information safe as we'll be using it in the next step when we setup the Raspberry Pi.

---

### Alexa Gadget Device Setup & Registration

---

In this step we will configure our Raspberry Pi as a registered Alexa Gadget. This process will require you to have the following pre-setup.

* **Raspberry Pi 3 B+**: Setup with Rasbian preferably.
  * Remote access either via VNC or SSH
  * `git` installed (*sudo apt install git*)

Connect to the Raspberry Pi, in my case I'm using `ssh` by running the following:

***NOTE**: you might need to replace `raspberrypi.local` with the IP address of the Pi on your network. same goes with the username `pi` if you changed it.*

```bash
ssh pi@raspberrypi.local
```

Pull down the [alexa/Alexa-Gadgets-Raspberry-Pi-Samples](https://github.com/alexa/Alexa-Gadgets-Raspberry-Pi-Samples) GitHub repository by running the following command from the home directory on the Raspberry Pi. Once cloned we will also change directory into the folder.

```bash
# Clone repo
git clone https://github.com/alexa/Alexa-Gadgets-Raspberry-Pi-Samples

# Change directory
cd Alexa-Gadgets-Raspberry-Pi-Samples
```

Within the folder there is a `launch.py` file that we will be running in order to configure the gadget with the authorization we created earlier.

```bash
sudo python3 launch.py --setup
# +--------------------------------------------------------------------+
# |    .oooooooo.                888                                   |
# |   d8P'    'Y8b     .oooo.    888   .ooooo.  oooo    ooo  .oooo.    |
# |  888        888   'P  )88b   888  d88' '88b  '88b..8P'  'P  )88b   |
# |  888        888    .oP'888   888  888ooo888    Y888'     .oP'888   |
# |  '88bb    dd88'   d8(  888   888  888    .o  .o8''88b   d8(  888   |
# |   'Y8bb,ood8P'    'Y888888o  888o 'Y8bod8P' o88'   888o 'Y888888o  |
# +--------------------------------------------------------------------+

# Do you want to configure all examples with your Alexa Gadget credentials (y/n)?
y

# Enter the Amazon ID for your gadget:
A30XXXXXXXXXXX

# Enter the Alexa Gadget Secret for your gadget:
4B4DXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

The process will go through and install / configure all the dependencies needed to run the Alexa Gadget service on the Pi. This includes but not limited to:

* protobuf
* Bluetooth (Low Energy)
* Python GPIO lib

***NOTE**: During the instllation you will be prompted to agree with the Terms and Conditions of the `bluez` package. you can do this by typing **AGREE** when asked to*

```bash
# The Alexa Gadgets Raspberry Pi launch script provided herein will retrieve the 'Bluez-5.50' package at install-time from third-party sources. There are terms and conditions that you need to agree to abide by if you choose to install the 'Bluez-5.50' package (https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/COPYING?h=5.50). This script will also enable you to modify and install the 'bluez-5.50' package to enable notification callbacks after reconnections to a paired Echo device. This is required for communication between your gadget and the Echo device over BLE. If you do not agree with every term and condition associated with 'Bluez-5.50', enter 'QUIT', else enter 'AGREE'.
AGREE
```

The last thing you will be asked is if you would like to run the communication transport in BT (Classic Bluetooth) or BLE (Bluetooth Low Energy) mode. Depedending on what Alexa device you have will dictact which mode to choose. [Here's a helpful list](https://developer.amazon.com/en-US/docs/alexa/alexa-gadgets-toolkit/understand-alexa-gadgets-toolkit.html#devices) of devices and their support you can refer to.

```bash
# Which transport mode would you like to configure your gadget for (ble/bt)?
ble
# +------------------------------+
# |            SUCCESS           |
# +------------------------------+
```

Congratulations! You've finished setting up the Alexa Gadget device. We can now move onto writing code to handle Alexa invocations.

---

### Gadget Code Explained

---

Okay, so you have a Raspberry Pi ready to become a gadget, but we still don't understand how Gadgets work. Let's dive into how we can structure a simple one.

At the heart of any Gadget project is the following folder and two files. For the sake of simpliciy, put this folder along side the other examples in [alexa/Alexa-Gadgets-Raspberry-Pi-Samples](https://github.com/alexa/Alexa-Gadgets-Raspberry-Pi-Samples).

```bash
|-- Alexa-Gadgets-Raspberry-Pi-Samples/src/examples
    |-- project_name
        |-- project_name.ini
        |-- project_name.py
```

* **project_name.ini**: Defines gadget details and permission scope
* **project_name.py**: Code that runs and interacts with Alexa over Bluetooth

#### project_name.ini

The project `.ini` file will contain the Amazon ID and Secret that you retrieved from the product creation step above; along with a set of capabilties.

```bash
[GadgetSettings]
amazonId = A30XXXXXXXXXXX
alexaGadgetSecret = 4B4DXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[GadgetCapabilities]
Notifications = 1.0
```

Each capability will expose a different event to the custom code you write later on in the `.py` file. It will make more sense in a second.

#### project_name.py

Below is a blank template for the capability file above. The functions defined below will be triggered when alexa receives each of the capabilies we subscribed to above.

```python
import logging
import sys

from agt import AlexaGadget

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('agt.alexa_gadget').setLevel(logging.DEBUG)

class ProjectNameGadget(AlexaGadget):

    def on_notifications_setindicator(self, directive):
        pass

    def on_notifications_clearindicator(self, directive):
        pass

if __name__ == '__main__':
    ProjectNameGadget().main()
```

An example might be that we would like to run some custom code to switch on an LED whenever an alarm finishes ringing. For this we could add some code to the `on_notifications_clearindicator` function like so

```python
...
    def on_notifications_setindicator(self, directive):
        RGB_LED.color = Color('red')

    def on_notifications_clearindicator(self, directive):
        RGB_LED.color = Color('green')
...
```

**NOTE**: *For information on other Gadget capabilities, [refer to the offical documentation](https://developer.amazon.com/en-US/docs/alexa/alexa-gadgets-toolkit/features.html).*

When you are ready to deploy the Gadget code and test functionality, run the following from the root folder inside [alexa/Alexa-Gadgets-Raspberry-Pi-Samples](https://github.com/alexa/Alexa-Gadgets-Raspberry-Pi-Samples).

```bash
sudo python3 launch.py --example project_name
```

#### Custom Directives

The final thing you will need to understand before looking at the cat feeder code is custom directives. These are similar to the capabilities above however instead of them coming from general alexa interactions, they are custom and fire into a user defined **namespace**.

An example would best be illustrated by first looking at how the normal directives function. Below is the payload that is captured when a notification comes through

```json
{
    "header":{
        "namespace":"Notifications",
        "name":"ClearIndicator",
        "messageId":"",
        "dialogRequestId":""
    },
    "payload":{

    }
}
```

See how the namespace `Notifications` matches the gadget capability we defined in the `project_name.ini` file. This means that we are able to define custom capabilities which become a namespace that can be utilized by our `project_name.py` code.

For example, lets use the example we'll also use later on called `CatFeederGadget`

```bash
[GadgetCapabilities]
Custom.CatFeederGadget = 1.0
```

We can now create functions in the code to handle any custom directives we'd like in the python code.

```python
# `CleanUp` function
def on_custom_catfeedergadget_cleanup(self, directive):
    pass
# `FeedCat` function
def on_custom_catfeedergadget_feedcat(self, directive):
    pass
```

When writing skill code later on we will be able to trigger these directives, or pass data to them by sending a json payload like below

```json
{
    "type": "CustomInterfaceController.SendDirective",
    "header": {
        "name": "FeedCat",
        "namespace": "Custom.CatFeederGadget"
    },
    "endpoint": {
        "endpointId": "<endpointId>"
    },
    "payload": {}
}
```

**NOTE**: *Some of the information above might now quite make sense yet, but once we've linked all the skill code and gadget code together it will start to become clear.*

---

### Cat Feeder Gadget Code

---

Now that you have a basic understanding of how Gadget code works we can begin to design our cat feeder. Below is the design for how the Alexa skill will operate once completed.

![Alexa Skill Pipeline](img/alexa-pipeline.png)