Cappuccino has been very successful at preserving the customary 'code and refresh' workflow for web developers. However, as any developer with more than a handful of cibs knows, having to manually run nib2cib breaks this workflow. Autonib2cib will solve this problem by automating the nib2cib process.

# Installation

autonib2cib requires pyfsevents and baker. Both can be installed with easy_install.

** pyfsevents **: `easy_install pyfsevents`

** baker **: `easy_install baker`

** Note **: pyfsevents installation fails when XCode 4 is installed. If you have XCode 4 installed use [these](https://github.com/klaaspieter/autonib2cib/wiki/XCode-4-installation) instructions.


# Usage

Run `python autonib2cib.py <PATH>`