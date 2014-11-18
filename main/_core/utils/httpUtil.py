#coding=utf-8
'''
Created on 2013-5-16
@author: Beni
'''
import mimetypes
import urllib.request



def httpGet(url):
    '''通过http的get请求获取数据'''
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
    return opener.open(url).read()



def httpPost(url, dataDict=None, fileDict=None, boundary='xxxxxx'):
    ''''通过http的post请求数据，可带参数和文件'''
    lines = []
    if dataDict != None:
        for name in dataDict:
            lines.extend ((
                           '--' + boundary,
                           '\r\n',
                           'Content-Disposition: form-data; name="{0}"'.format(name),
                           '\r\n\r\n',
                           str(dataDict[name]),
                           '\r\n'
                           ))
    if fileDict != None:
        for name in fileDict:
            lines.extend((
                           '--' + boundary,
                           '\r\n',
                           'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(name, fileDict[name]),
                           '\r\n',
                           'Content-Type: ' + (mimetypes.guess_type(fileDict[name])[0] or 'application/octet-stream'),
                           '\r\n\r\n',
                           open (fileDict[name], 'rb').read (),
                           '\r\n'
                          ))
    lines.extend ('--{0}--\r\n'.format(boundary))
    body = b''
    for x in lines:
        if(type(x) == str):
            body += x.encode()
        else:
            body += x
    headers = {
               'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
               'Content-Length': str (len(body))
               }
    result = urllib.request.Request (url, body, headers)
    response = urllib.request.urlopen(result)
    return response
