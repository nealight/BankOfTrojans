#!/bin/bash

# To run script:
#   ~#chmod +x recon.sh
#   ./recon.sh <IP>

# If no argument is passed, print usage example and exit
if [-z "$1"]
then
    echo "Usage: ./recon.sh <IP>"
    exit 1
fi

# Write output to text file called recon_results
printf "\n----- NMAP -----\n\n" > recon_results

# Run nmap intense scan (can alter this depending on situation)
#   https://www.securesolutions.no/zenmap-preset-scans/
# Takes argument and IP address and appends result to recon_results
# Remove tail/head lines for formatting purposes
echo "Running Nmap..."
nmap -T4 -A -v $1 | tail -n +5 | head -n -3 >> recon_results

# Attempt to enumeraete HTTP
# - run Gobuster
# - run WhatWeb
while read line
do
    # Check if open HTTP port found
    if [[$line == *open*]] && [[$line == *http*]]
    then
        echo "Running Gobuster..."
        # Takes -u specified IP address and -w specified wordlist and writes to temp file
        gobuster dir -u $1 -w /usr/share/wordlists/dirb/common.txt -qz > temp1
    echo "Running WhatWeb..."
    # takes IP address and writes verbose output to second temp file
    whatweb $1 -v > temp2
    fi
done < recon_results

# Check if temp files exist, writes temp file contents to results and removes temp
if [-e temp1]
then
    printf "\n----- DIRS -----\n\n" >> recon_results
    cat temp1 >> recon_results
    rm temp1
fi

if [-e temp2]
then
    printf "\n----- WEB -----\n\n" >> recon_results
    cat temp2 >> recon_results
    rm temp2
fi

cat results

# Code from:
# https://null-byte.wonderhowto.com/how-to/write-your-own-bash-script-automate-recon-0302808/
