import ftplib
import threading
import GlobalVar

class ThreadClass(threading.Thread):
    def run(self):
        ftp = ftplib.FTP("ftp.mvfbla.org")
        ftp.login("billzhou@mvfbla.org", "admin")
        ftp.cwd("ElValedor/Yearbook/")

        file = open(GlobalVar.UPLOADLOG_LOCATION,'rb')
        ftp.storbinary('STOR Uploadlog.txt', file)     # send the file
        file.close()
        ftp.quit()