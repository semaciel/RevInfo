#! /usr/bin/env python3
'''
Created By: SMAC
Description: Core Functions

'''
import sys
import os
import time
import os
import signal
import subprocess
import pathlib
import datetime
import getpass
#import apt
import io
import netifaces
import configparser
import requests
import json

# =============================================================
# =    			        Support                               =
# =============================================================

clear = lambda: os.system('cls' if os.name=='nt' else 'clear') # Windows Safe
#clear()

def signal_handler(signal, frame):
    clear()
    print ('=============================================================')
    print('\n\n >>> Good Bye!! [Ctrl+C Pressed] !!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def quitter():
    clear()
    print ('=============================================================')
    print('\n\n >>> Good Bye!! [Q Pressed] !!')
    sys.exit(0)

def pause():
	input('Please press any key to continue...')

def cur_time():
	now = datetime.datetime.now()
	temp = str(now.year) + "-" +  str(now.month) + "-" + str(now.day)
	return temp

def countdown(string, count):
    while count:
        mins, secs = divmod(count, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(string + "["+ timeformat + "]", end='\r')
        time.sleep(1)
        count -= 1
    print('Continue..\n\n\n\n\n')

def install_and_import(package):
	import importlib
	try:
		print("Checking if [" + package + "] package is available...")
		importlib.import_module(package)
	except ImportError:
		print("[" + package + "] Package not installed. Installing...")
		import pip
		pip.main(['install', package])
	finally:
		print("Retry import of [" + package + "] package after install...")
		globals()[package] = importlib.import_module(package)

def sudo_cmd(cmd):
    print ('=============================================================')
    cmd = "sudo " + cmd
    print (" cmd>> [" + cmd +"]")
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

def cmd(cmd):
    #print ('=============================================================')
    cmd = cmd
    print (" cmd>> [" + cmd +"]")
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

def run(cmd):
    #print ('=============================================================')
    cmd = cmd
    print (" cmd>> [" + cmd +"]")
    proc = subprocess.Popen(cmd + " &", shell=True)
    #proc.wait()

def dpkg_install(dpkgname):
    print ('=============================================================')
    sudo_cmd("dpkg -i " + CURDIR + dpkgname)
    apt_install("-f")

def apt_install(title):
	print ('=============================================================')
	print (" cmd>> apt_install(" + title + ")")
	#subprocess.check_call(['apt-get', 'install', '-y', 'filetoinstall'],stdout=open(os.devnull,'wb'), stderr=STDOUT)
	#subprocess.check_call(['sudo', 'apt-get', 'update'], stdout=open(os.devnull,'wb'), stderr=subprocess.STDOUT)
	proc = subprocess.Popen('sudo apt-get install -y ' + title, shell=True)
	proc.wait()

def purge(aptname):
    print ('=============================================================')
    cmd = "sudo apt-get purge -y " + aptname
    print (">>> Purging [" + aptname +"]")
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

def clean_temp():
	print ('=============================================================')
	print(">>> Cleanup Temp files")
	cmd("rm temp_*")
	cmd("ls -la temp_*")
	cmd("ls -la test_*")

def clean_duplicate_file(infilename, outfilename):
	lines_seen = set() # holds lines already seen
	outfile = open(outfilename, "w")
	for line in open(infilename, "r"):
	    if line not in lines_seen: # not a duplicate
	        outfile.write(line)
	        lines_seen.add(line)
	outfile.close()

def cfg_read(filein, section, field):
	#print ('=============================================================')
	#print (" cmd>> cfg_read()")
	config_r = configparser.ConfigParser()
	#config_r
	if config_r.read(filein) != []:
		#print("File Found")
		output = config_r.get(str(section),str(field))
		#print ("file:" + file)
		#print ("out: " + config_r.get(str(section),str(field)))
		return output
	else:
		#sys.exit(0)
		clear()
		print ('=============================================================')
		print("file:" + filein)
		print('\n\n >>> Good Bye!! [File Does not Exist] !!')
		sys.exit(0)

def cfg_sect2dict(filein, section):
    config= configparser.ConfigParser()
    config.read(filein)
    tempdict = dict(config.items(section))

    # Convert dict to 2 column list
    table = []
    for key, value in tempdict.items():
        newitem = [key,value] # grab key:value pair
        table.append(newitem) # add value:pair to out table

    return table

def cfg_write(filein, section, field, value):
	#sudo_cmd("cp " +CURDIR+"config.ini " +CURDIR+"temp_sudowrite")
	config= configparser.ConfigParser()
	config.read(filein)
	config.set(section,field,str(value))
	with open(filein, 'w+') as configfile:
		config.write(configfile)

def read_properties_file(file_path):
    with open(file_path) as f:
        config = io.StringIO()
        config.write('[dummy_section]\n')
        config.write(f.read().replace('%', '%%'))
        config.seek(0, os.SEEK_SET)

        cp = configparser.SafeConfigParser()
        cp.readfp(config)

        return dict(cp.items('dummy_section'))

def json_dump(dump):
    print(json.dumps(dump, indent=4, sort_keys=True))

def test_core():
	clear()
	#unit_info()
	pause()
	print("cur_time(): " + cur_time())
	countdown("test.. 8sec ", 8)
	print("cur_time(): " + cur_time())

	#def install_and_import(package):
	install_and_import("os")

	#####cmds
	# def sudo_cmd(cmd):
	# def cmd(cmd):
	# def run(cmd):

	sudo_cmd("hello")
	cmd("hello")
	run("hello")

	######installers
	# def dpkg_install(dpkgname):
	# def apt_install(title):
	# def purge(aptname):

	#dpkg_install("hello")
	purge("hello")
	apt_install("hello")

	#####fiel operations
	# def clean_temp():
	# def clean_duplicate_file(infilename, outfilename):
	# def cfg_read(file, section, field):
	# def cfg_write(file, section, field, value):
	# def read_properties_file(file_path):
	#         return dict(cp.items('dummy_section'))
	# def cfg_create():
	# def countdown(string, count):

	clean_temp()
	#clean_duplicate_file(infilename, outfilename):
	#cfg_read(file, section, field):
	#cfg_write(file, section, field, value):


    ## formatted Print
	json_dump('["foo", {"bar":["baz", null, 1.0, 2]}]')

	CURDIR = os.getcwd()+"/"
	print ("CURDIR: " +CURDIR)
	HOMEDIR = str(pathlib.Path.home())+"/"
	print ("HOMEDIR: " +CURDIR)
	#unit_info()
	print("Dict Output: " + str(read_properties_file(HOMEDIR+".zcash/zcash.conf")))
	cfg_create(HOMEDIR+".zcash/zcash.conf", CURDIR + 'config.ini')


if __name__ == "__main__":
	test_core()
