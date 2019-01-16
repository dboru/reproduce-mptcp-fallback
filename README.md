
# A script to reproduce mptcp fallback problem  

How to run 
-----------------
sh run-test.sh (root)

<<<<<<< HEAD
Dependencies to run the test
------------------------------

Mininet (version 2.3.0d1), Ryu SDN controller, MPTCP kernel(v0.94), python (2.7), Ubuntu 16.04 (4.14.79 )

Ryu installation
---------------------

pip install ryu 

OR git clone git://github.com/osrg/ryu.git cd ryu; pip install


How to run 
-----------------

sh run-test.sh (root)

MPTCP path manager and number of subflows can be changed in the python script (mfull-messh.py)
=======
MPTCP path manager and number of subflows can be changed in the python script (mfull-messh.py)

Dependencies
///////////////////////
>>>>>>> f531530a00002d686244e61fa4e30d90b9d00711

1. Mininet (verison 2.3.0d1)
2. Ryu SDN controller (pip install ryu or git clone git://github.com/osrg/ryu.git ; cd ryu; pip install 
3. MPTCP kernel (v0.94), python (2.7), Ubuntu 16.04 (v 4.14.79)

Trace dump from my test is available in https://github.com/dboru/reproduce-mptcp-fallback/blob/master/output/files-pcap.tar.gz









 

