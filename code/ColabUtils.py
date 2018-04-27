# Madhur Kashyap (madhurDOTkashyap  gmail)
# Google Colaboratory Utilities for running projects on colab
# Updated: Apr 27 2018


import re
import os
import sys
import subprocess
import tensorflow as tf

def git_clone(user,project,base_url='https://github.com',codedirs=[],
              verbose=False):
    url = '/'.join([base_url,user,project])
    status = subprocess.call(['rm', '-rf', project])
    status = subprocess.call(['git', 'clone', url]);
    cwd = os.getcwd();
    update_path([os.path.join(cwd,project,cdir) for cdir in codedirs]);

def update_path(codedirs):
    for cdir in codedirs:
        if os.path.exists(cdir):
            if cdir not in sys.path:
                sys.path.append(cdir);
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

def run_shell_commands(cmdlist,delim='+'*40,echo=True):
    for cmd in cmdlist:
        if echo: print(delim);
        log=subprocess.check_output(cmd);
        if echo: print(log.decode());
    if echo: print(delim)
    
def report_resources():
    cmdlist=[
        ['df','-h'],
        ['grep','-i','mem','/proc/meminfo'],
        ['grep','-i','cpu','/proc/cpuinfo'],
    ]
    run_shell_commands(cmdlist);

def authenticate():
    from google.colab import auth
    from oauth2client.client import GoogleCredentials
    print("Performing Google Account authentication for session ...")
    auth.authenticate_user()

def install_packages(pkgs):
    for pkg in pkgs:
        print("Installing package "+pkg+" ...");
        cmd=[sys.executable, '-m', 'pip', 'install', pkg]
        status = subprocess.call(cmd)
        if status!=0:
            print("Errors detected during package installation");

def setup_gdrive():
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    from google.colab import auth
    from oauth2client.client import GoogleCredentials
    print("Configuring Google Drive ...")
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    # An interactive procedure -- asks to go to a webform and get
    # Session specific authentication
    drive = GoogleDrive(gauth)
    return drive

def gdrive_download(drive,filepath,fileid,deflate=True):
    file1 = drive.CreateFile({'id':fileid});
    file1.GetContentFile(filepath);
    if deflate:
        if re.match('\.tar\.gz|.tgz',filepath):
            cmd = ['tar', '-zxvf', filepath];
        elif re.match('\.tar$',filepath):
            cmd = ['tar', '-xvf', filepath];
        elif re.match('.zip',filepath):
            cmd = ['unzip', filepath];
        else:
            cmd = [];
        if len(cmd)>0:
            status = subprocess.call(cmd);
            if status>0:
                print('Failed to deflate '+str(cmd));
        else:
            print('File appears to be deflated');

def gdrive_upload(drive,filepath):
    file = drive.CreateFile()
    file.SetContentFile(filepath)
    file.Upload()
