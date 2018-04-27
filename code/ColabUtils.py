# Madhur Kashyap (madhurDOTkashyap  gmail)
# Google Colaboratory Utilities for running projects on colab
# Updated: Apr 27 2018


import re
import os
import sys
import subprocess
import tensorflow as tf
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

def authenticate():
    auth.authenticate_user()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    # An interactive procedure -- asks to go to a webform and get
    # Session specific authentication
    drive = GoogleDrive(gauth)

def git_clone(user,project,base_url='https://github.com',codedirs=[]):
    url = '/'.join([base_url,user,project])
    status = subprocess.call(['rm', '-rf', project])
    status = subprocess.call(['git', 'clone', url]);
    update_path(codedirs);

def update_path(codedirs):
    for cdir in codedirs:
        rdir = os.path.join(".",project,cdir)
        if os.path.exists(rdir):
            if rdir not in sys.path:
                sys.path.append(rdir);
        else:
            print('WARN: Specified code dir does not exist'+cdir)

def verify_gpu():
    device_name = tf.test.gpu_device_name()
    if device_name != '/device:GPU:0':
        print('GPU device not found')
        has_gpu = True
    else:
        print('Found GPU at: {}'.format(device_name))
        has_gpu = False
    return has_gpu

def report_resources():
    !echo '++++++++++++++++++++++++++++++++++'
    !df -h .
    !echo '++++++++++++++++++++++++++++++++++'
    !cat /proc/meminfo | grep -i mem
    !echo '++++++++++++++++++++++++++++++++++'
    !cat /proc/cpuinfo | grep -i cpu
    !echo '++++++++++++++++++++++++++++++++++'

def install_packages(pkgs):
    for pkg in pkgs:
        print("Installing package "+pkg+" ...");
        status = subprocess.call(['pip', 'install', '-U', '-q', pkg])
        if status!=0:
            print("Errors detected during package installation");

