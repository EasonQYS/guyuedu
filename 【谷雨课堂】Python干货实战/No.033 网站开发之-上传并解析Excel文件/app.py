# coding:utf-8
# 【谷雨课堂】干货实战 No.033 网站开发之-上传并解析Excel文件
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


@app.route("/api/upload",methods=['POST'])
def uploader():
    upload_file=upfile()
    if upload_file=='':
        return "您没有上传文件 <a href='/'>返回</a>"
    
    s="Excel文件内容<hr>"
    workbook = xlrd.open_workbook("static/upload/"+upload_file)
    sheet1_object = workbook.sheet_by_index(0)
    nrows = sheet1_object.nrows
    ncols = sheet1_object.ncols
    row_values = sheet1_object.row_values(rowx=0)
    print("rows=%d" % nrows)
    print("cols=%d" % ncols)
    s=s+"<li>共%d行%d列" % (nrows,ncols)

    s=s+"<table border=1><tr>"
    for ss in row_values:
        s=s+"<td>%s</td>" % (ss)
    s=s+"</tr>"

    for i in range(1,nrows):
        record=sheet1_object.row_values(rowx=i)
        s=s+"<tr>"
        s=s+"<td>"+record[0]
        s=s+"<td>"+record[1] 
        s=s+"</tr>"    
    
    s=s+"</table>"
    s=s+"<hr><a href='/'>返回</a>"
    return s



@app.route("/")
def index():
    return render_template("upload.html")

app.run()
