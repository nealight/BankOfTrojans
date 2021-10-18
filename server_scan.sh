#/bin/bash

HOST="localhost"

echo $HOST

printf "\n----- NMAP -----\n\n" > recon_server

echo "Running Nmap"

nmap -T4  $HOST | tail -n +5 | head -n -2 >> recon_server

while read line
do
    if [[ $line == *open* ]] && ! [[ $line = 22/tcp* ]] && ! [[ $line = 111/tcp* ]]
    then
        PORT=${line%/*}
        echo $PORT
        lsof -i :$PORT | tail -n +2>> server_processes
        cat server_processes
        while read proc
        do
            #PID=$( $proc | awk "{print $2}")


            PID=$(echo $proc | awk '{print $2}')
            kill $PID


        done < server_processes
        rm server_processes

        nc -l $PORT &
    fi


done < recon_server
rm recon_server
