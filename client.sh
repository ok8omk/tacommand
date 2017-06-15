#!/bin/sh
function tacall () {
    # get seatid 
    seatid=`ifconfig en0 inet                               |\
    sed -n -e "2p"                                  |\
    sed -E "s/	inet ([0-9\.]*).*/\1/"              |\
    sed -E "s/[0-9]*\.[0-9]*\.[0-9]*\.([0-9]*)/\1/"`
    METHOD="-X POST"
    while getopts hx opt
    do
        case ${opt} in
        h)
            echo "If you solve your problem by yourself after calling,";
            echo "execute \"tacall -x\"";
            exit 0;;
        x)
            METHOD="-X DELETE";;
        \?)
            exit 1;;
        esac
    done
    curl $METHOD http://0.0.0.0:5000/api/$seatid
}
