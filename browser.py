import socket
import ssl

def request(url):

    #Checking if your URL contains http or https
    scheme, url = url.split("://", 1)
    assert scheme in ["http", "https", "file"], "Unknown scheme {}".format(scheme)

    if ("/" in url):
        #Spliting the URL to the path(/index.html) and host(example.org)
        host , path = url.split("/",1)
        #need this
        path = "/" + path
    else:
        host = url
        path = '/'
    port = 80 if scheme == "http" else 443
            #support for custom port http://example.org:8080/index.html

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    s=socket.socket(
        family=socket.AF_INET,          #address family:tells us how to connect
        type=socket.SOCK_STREAM,        #tells us what kind of conversion is happenning.here we send and recieve arbitrary amounts of data
        proto=socket.IPPROTO_TCP        #steps to establish a connection
    )

    #connect to the host at post 80,connect takes a single argument, and that argument is a pair of a host and a port.
    s.connect((host , port))

    '''
    request a response to the website
    \r\n is the carriage return or newline used in HTML RCF2616 section 2.2
    \r\n is used for a newline as a rule by RCF2616 standard
    '''
    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    s.send("GET {} HTTP/1.0\r\n".format(path).encode("utf8") + 
        "Connection: {}\r\n".format("close").encode("utf8") +
        "User-Agent: {}\r\n".format("testbrowser").encode("utf8") +
        "Host: {}\r\n\r\n".format(host).encode("utf8"))

    #we make a file with the response
    #the response will be in bytes so we encode it into utf8
    response = s.makefile("r", encoding="utf8" , newline="\r\n")
    #print(response.read()) #try if you dont understand below

    #the first line of response is HTTP/1.0 200 OK
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    '''
    if assertion is false it will show the error code and its english expliantion
    we dont check the http version as some misconfigured serves reply with ver1.1 even when we ask for ver1.0
    both are similar so no issues
    '''
    assert status == "200", "{}: {}".format(status, explanation)

    #creating a dict with all headers and its values
    headers = {}
    while True:
        line = response.readline()
        if line == "\r\n": 
            break
        header, value = line.split(":", 1)
        #dict_name[pos1]=value 1 ==> pos1 : value
        #headers are case INSENSITIVE
        headers[header.lower()] = value.strip()

    #checking if data is sent in unusual way
    assert "transfer-encoding" not in headers
    assert "content-encoding" not in headers

    body = response.read()
    s.close()

    return headers, body

def show(body):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")

def load(url):
    headers, body = request(url)
    show(body)

if __name__ == "__main__":
    import sys
    load(sys.argv[1])
