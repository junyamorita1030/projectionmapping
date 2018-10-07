import urllib.request, os
from logging import getLogger

logger = getLogger(__name__)

class Webcam:
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = password
        logger.debug('オブジェクト生成')
        
    def setup_basic_auth(self):
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(
            realm=None,
            uri='http://%s:%s/' % (self.ip, self.port),
            user=self.user,
            passwd=self.passwd)
        auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(auth_handler)
        try:
            urllib.request.install_opener(opener)
            logger.debug('BASIC認証成功')
        except Exception as err:
            logger.exception('Error : %s', err)


    def take_picture(self, file_path):
        # convert relative path to absolute path
        path = os.path.abspath(file_path)
        url = 'http://%s:%s/snapshot.jpg' % (self.ip, self.port)
        try:
            pic = urllib.request.urlopen(url).read()
            with open(path, mode='wb') as f:
                f.write(pic)
            logger.debug('写真撮影成功')
        except Exception as err:
            logger.exception('Error : %s', err)

if __name__ == '__main__':
    wc = Webcam('ipaddress', 'port', 'user', 'passwd')
    wc.setup_basic_auth()
    wc.take_picture('snapshot.jpg')
