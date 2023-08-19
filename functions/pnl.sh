#!/bin/bash
sudo tcpdump -i wlan1 -e -nn 2> /dev/null | grep Probe | sed -rn 's/.* ([^\s]+) signal .*SA:(.+) Probe Request .*\(([^\)]+)\).*/\1 \2 \3/p'
