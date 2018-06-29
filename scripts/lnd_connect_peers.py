#!/usr/bin/env python
#
# Script to get a peer list from different url and connect automaticly
# just run as cronjob and watch your peer connects growing

import requests, subprocess, json, sys, os

devnull = open(os.devnull, 'wb')
urls = [ 'https://1ml.com/node?order=capacity&json=true',  
         'https://1ml.com/node?order=lastupdated&json=true', 
         'https://1ml.com/node?order=mostchannels&json=true']

peerCommand = "lncli listpeers"
process     = subprocess.Popen(peerCommand.split(), stdout=subprocess.PIPE)
peers       = json.loads(process.communicate()[0])
pub_keys    = []

for peer in  peers["peers"]:
    pub_keys.append(peer["pub_key"])

######################
#parse json from urls
######################

for url in urls:
    resp = requests.get(url)
    data = resp.json()
    #print "Get peers from %s" % url
    for line in data:
        if len(line["addresses"]) != 0:
            if line["pub_key"] not in pub_keys:
                bashCommand = "timeout 5 lncli connect %s@%s" % ( line["pub_key"], 
                                                                  line["addresses"][0]["addr"] 
                                                                )
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=devnull)
                streamdata = process.communicate()[0]
                #if process.returncode == 0:
                #    print "%s neu connected"  % ( line["pub_key"] )
                #else:
                #    print "%s returncode: %d" % ( line["pub_key"], int(process.returncode) )
            else:
                #print "%s bereits connected"  % ( line["pub_key"] )
                continue
        else:
            continue

#bashCommand = "lncli getinfo | grep peer"
#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#info, info_error = process.communicate()

#if info_error:
#    print info_error
#else:
#    print json.loads(info)["num_peers"]
