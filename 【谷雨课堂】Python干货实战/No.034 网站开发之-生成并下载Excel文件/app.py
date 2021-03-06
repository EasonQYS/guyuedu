# coding:utf-8
# 【谷雨课堂】干货实战 No.034 生成并下载Excel文件
# 作者：谷雨

from flask import Flask,url_for,redirect,render_template,request,Response
import time
import os
import io
import mimetypes
import xhtml2pdf.pisa as pisa
from werkzeug.datastructures import Headers
from urllib.parse import quote
import xlrd,xlwt

app = Flask(__name__)

#基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#static路径
STATIC_DIR = os.path.join(BASE_DIR,'static')

#上传路径
UPLOAD_DIR = os.path.join(STATIC_DIR,'upload')

# 上传文件处理,自动找上传的参数名
def upfile(field='',dir=''):
 
    if len(request.files)<1:
        return ""

    if field=='':
        for k in request.files:
            field=k
            break

    f = request.files[field]
    if f==None:
        print("没有上传的字段"+field)
        return ""
    fname = f.filename

    if fname=='':
        return ''

    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeStruct = time.localtime(now)
    str_ymd = time.strftime("%Y-%m-%d", timeStruct)
    if dir=='':dir=str_ymd
    if not os.path.exists(UPLOAD_DIR+"/"+dir):
        os.makedirs(UPLOAD_DIR+"/"+dir)
    print(UPLOAD_DIR+"/"+dir+'/'+new_filename)
    f.save(UPLOAD_DIR+"/"+dir+'/'+new_filename)
    return dir+'/'+new_filename



def http_download(stream,filename):
    response = Response()
    response.status_code = 200
    response.data = stream
    mimetype_tuple = mimetypes.guess_type(filename)
    response_headers = Headers({
            'Pragma': "public",  # required,
            'Expires': '0',
            'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
            'Content-Type': mimetype_tuple[0],
            'Content-Disposition': 'attachment; filename=\"%s\";' % quote(filename),
            'Content-Transfer-Encoding': 'binary',
            'Content-Length': len(response.data)
        })
    response.headers = response_headers
    return response



@app.route("/excel")
def excel():
    workbook = xlwt.Workbook(encoding = 'utf-8')
    ws = workbook.add_sheet('Sheet1')
    fields=['UserName','Password']
    idx=0
    for x in fields:
        ws.write(0,idx, x)
        idx=idx+1

    for i in range(1,101):
        ws.write(i,0, 'user'+str(i))
        ws.write(i,1, 'pass'+str(i))



    output = io.BytesIO()
    workbook.save(output)

    return http_download(output.getvalue(),"hn_users.xls")

@app.route("/")
def index():
    return "<a href='/excel'>导出Excel</a>"


app.run()
