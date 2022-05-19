# Imports
from netmiko import ConnectHandler
import sys
import csv
import time

# vEOS-1 dictionary
veos1 = {
    "device_type": "arista_eos",
    "host": "192.168.1.210",
    "username": "admin",
    "password": "int-2240",
    "secret": "int-2240"
}

# vEOS-2 dictionary
veos2 = {
    "device_type": "arista_eos",
    "host": "192.168.1.213",
    "username": "admin",
    "password": "int-2240",
    "secret": "int-2240"
}
    
# Linux server dictionary
linux_server = {
    "device_type": "linux",
    "host": "192.168.1.209",
    "ip": "192.168.1.209",
    "username": "gns3",
    "password": "gns3",
    "secret": "gns3"
}

# Imports CSV, reads info and stores
def importcsv():
    print("Importing CSV...")
    default_routes = {} # Store default routes
    default_gate = {} # Store default gateways
    ip = {} # Store IP addresses

    time.sleep(2) # Pause
    print("..") # Simulate pause

    # Open file and store info
    try:
        with open("design.csv", "r") as data:
            for line in csv.DictReader(data):
                if line["default route"] != "":
                    default_routes[line["Device"]] = line["default route"]
                if line["Default gateway"] != "":
                    default_gate[line["Device"]] = line["Default gateway"]
                if line["IP address"] != "":
                    ip[(line["Device"], line["Interface"])] = line["IP address"]
    except:
        # Pause and show success
        time.sleep(1.5)
        print("Success")
        time.sleep(2)

# This functions configures the second Arista switch
# @param veos2: vEOS-2 dictionary (second switch) 
def veos2config(veos2):
    # Try creating ConnectHandler object for vEOS-2
    try:
        print("Connecting to vEOS-2")
        net_connect = ConnectHandler(**veos2)
        print("SSH connection established")
        time.sleep(2)
    except:
        print("SSH failed")
        sys.exit()

    # Try configuring
    try:
        print("Sending commands to vEOS-2")
        net_connect.enable()
        print(net_connect.send_command("show ip int brief"))
        print(net_connect.find_prompt())

        net_connect.send_command_timing("configure terminal")
        print(net_connect.find_prompt())
        net_connect.send_command_timing("ip routing")
        net_connect.send_command_timing("interface Ethernet 4")
        net_connect.send_command_timing("no switchport")
        print(net_connect.find_prompt())
        time.sleep(2)
        
        net_connect.send_command("ip address 10.10.4.2/24")
        net_connect.send_command_timing("no shutdown")
        net_connect.send_command_timing("configure terminal")
        net_connect.send_command_timing("ip routing")
        net_connect.send_command_timing("interface Ethernet 3")
        net_connect.send_command_timing("no switchport")
        net_connect.send_command("ip address 10.10.3.2/24")
        net_connect.send_command_timing("no shutdown")
        net_connect.send_command_timing("configure terminal")
        net_connect.send_command_timing("ip routing")
        net_connect.send_command_timing("interface Ethernet 12")
        net_connect.send_command_timing("no switchport")
        net_connect.send_command("ip address 10.10.5.2/24")
        net_connect.send_command_timing("end")
        print(net_connect.send_command_timing("show ip route"))
        print(net_connect.find_prompt())
        net_connect.send_command("copy run start")
        net_connect.exit_enable_mode()
        print(net_connect.find_prompt())
        time.sleep(2)

        output = net_connect.send_command("show ip int brief")
        print("------------vEOS-2---------")
        print(output)
        net_connect.disconnect()
        time.sleep(2)
    except:
        print("Command failed")
        sys.exit()
    net_connect.disconnect()

# This function configures the first Arista switch
# @param veos1: vEOS-1 dictionary
def veos1config(veos1):
    # Try creating ConnectHandler object for vEOS-1
    try:
        print("Connecting to vEOS-1")
        net_connect = ConnectHandler(**veos1)
        print("SSH connection established")
        time.sleep(2)
    except:
        print("SSH failed")
        sys.exit()

    # Try configuring
    try:
        print("Sending commands to vEOS-1")
        net_connect.enable()
        print(net_connect.send_command("show ip int brief"))
        print(net_connect.find_prompt())

        net_connect.send_command_timing("configure terminal")
        print(net_connect.find_prompt())
        net_connect.send_command_timing("ip routing")
        net_connect.send_command_timing("interface Ethernet 1")
        net_connect.send_command_timing("no switchport")
        print(net_connect.find_prompt())
        time.sleep(2)
        
        net_connect.send_command("ip address 10.10.1.2/24")
        net_connect.send_command_timing("no shutdown")
        net_connect.send_command_timing("configure terminal")
        net_connect.send_command_timing("ip routing")
        net_connect.send_command_timing("interface Ethernet 2")
        net_connect.send_command_timing("no switchport")
        net_connect.send_command("ip address 10.10.2.2/24")
        net_connect.send_command_timing("no shutdown")
        net_connect.send_command_timing("configure terminal")
        net_connect.send_command_timing("ip routing")
        net_connect.send_command_timing("interface Ethernet 4")
        net_connect.send_command_timing("no switchport")
        net_connect.send_command("ip address 10.10.4.1/24")
        net_connect.send_command_timing("end")
        print(net_connect.send_command_timing("show ip route"))
        print(net_connect.find_prompt())
        net_connect.send_command("copy run start")
        net_connect.exit_enable_mode()
        print(net_connect.find_prompt())
        time.sleep(2)

        output = net_connect.send_command("show ip int brief")
        print("------------vEOS-1---------")
        print(output)
        net_connect.disconnect()
        time.sleep(2)
    except:
        print("Command failed")
        sys.exit()
    net_connect.disconnect()

# This function configures the linux server
# @param linux_server: linux server dictionary
def linuxconfig(linux_server):
    # Try creating ConnectHandler object for linux server
    try:
        print("Connecting to Linux server")
        net_conn = ConnectHandler(**linux_server)
        print("SSH Connection established")
        time.sleep(2)        
    except Exception:
        print("SSH failed")
        sys.exit()

    # Try configuring
    try:
        net_conn.enable(cmd = "sudo su", pattern = "password")
        net_conn.send_command("ip addr add 10.10.5.1 dev ens4")
        net_conn.send_command("ip route add default via 10.10.5.2 dev ens4")
        result = net_conn.send_command("ip address show")
        print(net_conn.send_command("ip route show"))
        print("----------------OUTPUT---------------")
        print(result)

        with open("server.txt", "w") as f:
            f.write(result)
        net_conn.exit_enable_mode()
        print("\nCompleted\n")
        time.sleep(2)
    except:
        print("Failed")
        sys.exit()
    net_conn.disconnect()

# Main config function (calls sub configurations)
def config_gen():
    linuxconfig(linux_server)
    veos1config(veos1)
    veos2config(veos2)

# Test connectivity
# @param num: a given vEOS-n switch (n = 1 or n = 2)
# @param add: a given ip address
def test_con(num, add):
    # If first switch
    if (num == 1):
        try:
            conn = ConnectHandler(**veos1)
        except:
            print("Failed")
            sys.exit()
    # If second switch
    elif (num == 2):
        try:
            conn = ConnectHandler(**veos2)
        except:
            print("Failed")
            sys.exit()

    # Test connectivity
    pingcheckarp = "ping " + add
    pingcheck = "ping " + add
    conn.send_command(pingcheckarp)
    pingresult = conn.send_command(pingcheck)

    # Print results
    if "0% packet loss" in pingresult:
        print("Successful ping")
    else:
        print("Ping failed")

# Collect information and store in text files
def collect_info(veos1, veos2, linux_server):
    # Get vEOS-1 info
    net_conn = ConnectHandler(**veos1)
    net_conn.enable()
    net_conn.send_command_timing("configure terminal")
    result = net_conn.send_command_timing("show run")
    # Store info
    with open("veos-1_conf.txt", "w") as f:
            f.write(result)
    net_conn.disconnect()

    # Get vEOS-2 info
    net_conn2 = ConnectHandler(**veos2)
    net_conn2.enable()
    net_conn2.send_command_timing("configure terminal")
    result = net_conn2.send_command_timing("show run")
    # Store info
    with open("veos-2_conf.txt", "w") as f:
            f.write(result)
    net_conn2.disconnect()

    # Get linux server info
    net_conn3 = ConnectHandler(**linux_server)
    net_conn3.enable(cmd = "sudo su", pattern = "password")
    net_conn3.send_command_timing("configure terminal")
    result = net_conn3.send_command_timing("ip address show")
    # Store info
    with open("server_net.txt", "w") as f:
            f.write(result)
    net_conn3.disconnect()

# If module is ran
if __name__ == "__main__":
    config_gen() # Run configuration function
    collect_info(veos1, veos2, linux_server) # Collect info