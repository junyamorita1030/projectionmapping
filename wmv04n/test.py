from wmv04n import Webcam

if __name__ == '__main__':
    wc = Webcam('ipaddress', 'port', 'user', 'passwd')
    wc.setup_basic_auth()
    wc.take_picture('snapshot.jpg')
