#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Controller, RemoteController, OVSKernelSwitch, CPULimitedHost
from mininet.cli import CLI

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom

from mininet.log import setLogLevel, info
from simpletopo import simpleTopo
from random import choice, shuffle,randint,randrange,uniform
from threading import Timer
import os
from time import sleep,time
import random


def readTrace():
    trace=[]
    with open("./Trace-Generator/trace_file/output.trace") as fp:
        lines = fp.readlines()
        for line in lines:
            trace.append(line.split())
    return trace


def disableOffloading(net):
    nodes = net.switches+net.hosts
    for node in nodes:
        node.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        node.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        node.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
        for port in node.ports:
            if str.format('{}', port) != 'lo':
                #node.cmd(str.format('ethtool --offload {} tx off rx off gro off tso off', port))
                node.cmd(str.format('ethtool -K {} gso off tso off gro off tx off rx off', port))
                

def enableMPTCP(subflows):
    os.system("sudo sysctl -w net.ipv4.tcp_ecn=0")
    os.system("sudo sysctl -w net.mptcp.mptcp_enabled=1")
    os.system("sudo sysctl -w net.mptcp.mptcp_debug=1")
    os.system("sudo sysctl -w net.mptcp.mptcp_path_manager=fullmesh")
    os.system("sudo echo -n %i > /sys/module/mptcp_fullmesh/parameters/num_subflows" % int(subflows))
    os.system("sudo sysctl -w net.ipv4.tcp_congestion_control=olia")



def send_request(client, server,flowsize,output_dir='output'):
	client.popen("./client-server/bin/simple-client -s  %s  -p 6201  -n %d -c 1 >> %s/flow_fct_clnt%s_serv%s &" % \
		(server.IP(),flowsize, output_dir,client.IP(),server.IP()),shell=True)

topo = simpleTopo()

link = custom(TCLink, bw=10,delay='1ms',max_queue_size=100)

net = Mininet(topo,link=link, switch=OVSKernelSwitch,controller=RemoteController, autoStaticArp=True)

net.start()
# enable MPTCP
enableMPTCP(4)
# disable IPv6 and offloading
disableOffloading(net)

hosts=net.hosts

# start servers 
for server in hosts:        
   # servport=random.randrange(1000,60000)
   # servport=5001
   # server_port_map[sserver]=servport
   # server.cmd( "./client-server/bin/server -p %s  >> /dev/null & " % servport)
   server.cmd( "./client-server/bin/server -p 6201  >> /dev/null & ")
sleep(5)


os.system('rm output/trace* output/flow_fct*')

# dump traffic from hosts

for host in hosts:
	for port in host.ports:
		if port !='lo':
			host.popen("tcpdump -i %s -s 96 -w %s/trace-%s.pcap"%(port,'output',host.IP()), shell=True)

trace=readTrace()
count=0
for conn in trace:
    count=count+1
    if count > (len(trace)-1):
        break
    client=None
    server=None
    for h in hosts:
        if h.IP()==conn[1]:
           client=h
        if h.IP()==conn[2]:
           server=h
        if client and server:
           break
    flowsize=int(conn[5])
    cur_start_time=float(conn[6])
    next_request=trace[count]
    next_time=float(next_request[6])
     
    Timer(cur_start_time, send_request,(client,server,flowsize,'output')).start()
    # if count > 20:
    # 	break
sleep(5)

while True:
	clnt=os.popen("ps ax | grep simple-client | wc -l").read()
	nclnt=clnt.split('\n')
	if  len(nclnt) == 2 and int(nclnt[0]) < 4:
		os.system('killall -9 simple-client server iperf tcpdump')
		break;
	else:
		sleep(1)

net.stop()
