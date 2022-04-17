import socket
from pathlib import Path
import os
import os.path

def serv():
    s_s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port=60000
    s_s.bind(('localhost',port))
    s_s.listen(5)
    print("Starting connection at port: ",port)
    conn,adrs=s_s.accept()
    print("Connection established with ",adrs)
    buf=conn.recv(2048)
    buf=buf.decode()
    req=buf.split()
    method=req[0]
    cpath=req[1]
    fpath=cpath[1:]



    def GET():
        print("HTTP Request: \n",buf)
        if(os.path.exists(fpath)):
            if(content_type()=="text/html"):
                with open(fpath,'r') as f:
                    page=f.read()
                respond="HTTP/1.1 200 OK\n"
                respond=respond+"Content-Type: "+content_type()+"\r\n"
                respond=respond+"Content-Length: "+str(len(page))+"\r\n"
                respond=respond+"\r\n"
                respond=respond+page
                print("HTTP Respond: \n",respond)
                respond=bytes(respond,'UTF-8')
                conn.sendall(respond)
                f.close()
            else:
                msg="Sorry, not supported yet!\nTry localhost:%s/a.html"%port
                conn.sendall(msg.encode())
        else:
            with open('404.html','r') as not_found:
                page=not_found.read()
            respond="HTTP/1.1 404 Not Found\n"
            respond=respond+"Content-Type: text/html\r\n"
            respond=respond+"Content-Length: "+str(len(page))+"\r\n"
            respond=respond+"\r\n"
            respond=respond+page
            print("HTTP Respond \n",respond)
            respond=bytes(respond,'UTF-8')
            conn.sendall(respond)
            not_found.close()


    def content_type():
        if(Path(fpath).suffix=='.html' or Path(fpath).suffix=='txt'):
            return "text/html"
        elif(Path(fpath).suffix=='png'):
            return "image/png"
        elif(Path(fpath).suffix=='jpg' or Path(fpath).suffix=='jpeg'):
            return "image/jpeg"
        else:
            return "application/octet-stream" 



    if (method=="GET"):
        GET()
    else:
        msg="Sorry, not supported yet!"
        conn.sendall(msg.encode())


    print("Closing connection...")
    s_s.close()

while(True):
    serv()
    




# alternate http server using python modules:
# import socketserver
# from http.server import SimpleHTTPRequestHandler


# host="localhost"
# port=9999
# handler=SimpleHTTPRequestHandler


# if __name__ == "__main__":
#     serv=socketserver.TCPServer((host,port),handler)
#     print("server started %s:%s"%(host,port))


#     try:
#         serv.serve_forever()
#     except KeyboardInterrupt:
#         pass;

#     serv.server_close()
#     print("stopping server...")

# also we can run this in termianl and get a simple http server:
# python -m http.server {port number}    python3
# python -m SimpleHTTPServer {port number}   python3