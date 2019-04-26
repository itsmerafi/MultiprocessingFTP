import socket, sys, json, os

HOST = '127.0.0.1'
PORT = 1060

def recvall(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message'
                           % (len(data), length))
        data += more
    return data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print 'connected via:', s.getsockname()

while True:
    inp = raw_input('user$ ' )
    res = inp.split()
    cmd = res[0].upper()
    if len(res)>1:
        js = {'cmd':cmd, 'arg':res[1]}
    else:
        js = {'cmd':cmd, 'arg': "*" }
    js2 = json.dumps(js)
    #print js

    if cmd == "LS":
        s.sendall(js2)
        print 'List Dir : '
        reply = s.recv(2048) # Get list dir
        
        print reply

    elif cmd=="GET":
        if len(res)<2:
            print "File Undifined!"
        else :
            s.sendall(js2)
            reply = s.recv(2048)
            reply = json.loads(reply)
            if reply['Preparing'] == "Preparing a file":
                print 'Server : ', repr(reply['Preparing'])
                size = reply['size']
                print 'File Size Download : ', size + "bit"

                
                f = open("client/" + res[1], 'wb+')
                f.write(reply['read'])
                f.close()

                status = reply['status']
                print 'Server :', repr(status)
            else :
                print 'Server : ', repr(reply['Preparing'])

    elif cmd == "PUT":
        if len(res)<2:
            print "File Undifined!"  

        elif os.path.exists("client/"+res[1]):
            filepath = "client/"+res[1]
            print "Filepath : " + filepath
            # s.sendall(js2)
            # discard return value
            
            read = open(filepath,'rb').read() #readfile
            send_file = len(read) #size file
            print 'File Size Upload : ', send_file 
            js['size'] = str(send_file) # send size file
            js['read'] = read # send file
            js2 = json.dumps(js)
            s.sendall(js2)
            reply = s.recv(2048) # discard return value
            print 'Server : ', repr(reply)

        else :
            print "File Not Found!"

    elif cmd == "QUIT":
        s.sendall(js2)
        reply = s.recv(1024)
        print 'Server : ', repr(reply)
        print 'Close connection..'
        s.close()
        exit(0)
    else:
        print "Unknown command.."

