from datetime import datetime
import shutil
import sys, os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import schedule
import logging

def create_zip(path, file_name):
    # use shutil to create a zip file
    try:
        shutil.make_archive(f"archive/{file_name}", 'zip', path)
        return True
    except FileNotFoundError as e:
    	return False

def google_auth():
    gauth = GoogleAuth() 
    # use local default browser for authentication
    gauth.LocalWebserverAuth()        
    drive = GoogleDrive(gauth) 
    return gauth, drive

def upload_backup(drive, path, file_name):

    # create a google drive file instance
    f = drive.CreateFile({'title': file_name}) 

    # set the path to zip file
    f.SetContentFile(os.path.join(path, file_name)) 

    # start logging
    logging.basicConfig(filename="log.log",format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    try:
    	f.Upload() 
    	logger.critical("backup_successful "+os.path.join(os.getcwd(),path, file_name))
    except Exception as e:
    	logger.critical("backup_failed "+e.__class__)
    
    # f is set to none because of a vulnerability found in PyDrive
    f = None

def controller():
    # folder path to backup
    path = "./summary"
    now = datetime.now()
    # new backup name
    # file_name = str("backup_" + now.strftime(r"%d/%m/%Y_%H:%M:%S").replace('/', '-'))
    # if zip creation fails then abort execution
    if  not create_zip(path, "riya"):
    	sys.exit(0)
    auth, drive = google_auth()
    upload_backup(drive, r"archive", "riya"+'.zip')

if __name__=="__main__":
    # set 12:00 am as time to trigger controller check for pending tasks and execute if any
    # controller()
    schedule.every().day.at("00:00").do(controller)
    while True:
        schedule.run_pending()