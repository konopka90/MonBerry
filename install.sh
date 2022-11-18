#!/bin/bash

if ! [ "$(id -u)" = 0 ];then
	echo "You must be root to perform this action."
	exit
fi
	
mkdir -p /opt/MonBerry
cp show-dashboard.sh /opt/MonBerry/
cp show-dashboard.service /lib/systemd/system/
sed -i "s/User=/User=${SUDO_USER}/g" /lib/systemd/system/show-dashboard.service
sed -i "s/Group=/Group=${SUDO_USER}/g" /lib/systemd/system/show-dashboard.service
chown -R $SUDO_USER: /opt/MonBerry
systemctl daemon-reload
systemctl enable show-dashboard.service
systemctl restart show-dashboard.service
