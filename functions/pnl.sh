#!/bin/bash
wlan="$1"
sudo tcpdump -i $wlan -e -nn 2> /dev/null | grep Probe | sed -rn 's/.* ([^\s]+) signal .*SA:(.+) Probe Request .*\(([^\)]+)\).*/\1 \2 \3/p'
