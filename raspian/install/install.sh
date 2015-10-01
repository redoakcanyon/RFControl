#!/bin/sh
cp libftd2xx.so.1.2.7 /usr/local/lib/libftd2xx.so.1.2.7
ln -s /usr/local/lib/libftd2xx.so.1.2.7 /usr/local/lib/libftd2xx.so
ldconfig
mkdir /var/RFControl
chmod a+w /var/RFControl
cp 99-libftdi.rules /etc/udev/rules.d/99-libftdi.rules
cp RFControl* /usr/local/bin/RFControl
