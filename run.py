# encoding=utf-8
import datetime
import os
import shutil
from PIL import Image
from flask import Flask, render_template, Response, request, redirect, url_for

app = Flask(__name__)


@app.route("/upload_row/", endpoint="upload_row", methods=["GET", "POST"])
def upload_row():
    """
    上传图片，保存到服务器本地
    文件对象保存在request.files上，并且通过前端的input标签的name属性来获取
    :return: 重定向到主页
    """
    fp = request.files.get("f1")
    if fp is not None:
        now_date = datetime.datetime.now()
        uid = now_date.strftime('%Y-%m-%d-%H-%M-%S')

        # 保存文件到服务器本地
        file = "./static/images/%s.jpg" % uid
        file_keep = "./static/images_keep/%s.jpg" % uid
        fp.save(file)
        shutil.copy(file, file_keep)

        with open(file, 'rb') as f:
            if len(f.read()) < 100:
                os.remove(file)
                pass
            else:
                im = Image.open(file)
                x, y = im.size
                y_s = int(y * 1000 / x)

                out = im.resize((1000, y_s), Image.ANTIALIAS)

                uid2 = now_date.strftime('%Y-%m-%d-%H-%M-%S')
                # 保存文件到服务器本地
                file2 = "./static/images/%s.jpg" % uid2
                if len(out.mode) == 4:
                    r, g, b, a = out.split()
                    img = Image.merge("RGB", (r, g, b))
                    img.convert('RGB').save(file2, quality=10)
                else:
                    out.save(file2)

    return redirect(url_for("love"))


@app.route("/pic", methods=["GET", "POST"])
def static_picture():
    """
    网页获取图片的接口，根据图片的名字来获取
    :return: 返回图片流
    """
    pic_name = request.args.get('name')
    file = request.args.get('file')
    file_name = './static/%s/%s' % (file, pic_name)
    # print(file_name)
    with open(file_name, 'rb') as f:
        content = f.read()
    resp = Response(content, mimetype="image/jpeg")
    return resp


@app.route("/delete", methods=["GET", "POST"])
def delete():
    """
    删除图片的接口，将图片存到images_delete文件夹里
    :return: 重定向到主页
    """
    pic_name = request.args.get('name')
    file_name = './static/images/%s' % pic_name
    file_name2 = './static/images_delete/%s' % pic_name
    shutil.move(file_name, file_name2)
    return redirect(url_for("love"))


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    添加图片的接口，将图片存到images文件夹里
    :return: 重定向到主页
    """
    pic_name = request.args.get('name')
    file_name = './static/images/%s' % pic_name
    file_name2 = './static/images_delete/%s' % pic_name
    shutil.move(file_name2, file_name)
    return redirect(url_for("miss"))


@app.route("/love", methods=["GET", "POST"])
def love():
    """
    主页，获取传递过去的图片所有信息
    :return: 返回主页html
    """
    pic_li = os.listdir('./static/images/')
    print(pic_li)
    pic_li.sort(reverse=True)
    a = datetime.datetime.now()
    a = a + datetime.timedelta(0.5)
    time_now = datetime.datetime.strftime(a, "%Y-%m-%d")
    context = {'name': "xiaohua", 'li': pic_li, "time": time_now}
    return render_template('home.html', context=context)


@app.route("/miss", methods=["GET", "POST"])
def miss():
    """
    回收站主页，获取回收站里的图片所有信息
    :return: 返回回收站主页html
    """
    pic_li = os.listdir('./static/images_delete/')
    print(pic_li)
    pic_li.sort(reverse=True)
    a = datetime.datetime.now()
    a = a + datetime.timedelta(0.5)
    time_now = datetime.datetime.strftime(a, "%Y-%m-%d")
    context = {'name': "xiaohua", 'li': pic_li, "time": time_now}
    return render_template('home_miss.html', context=context)


@app.route("/keep", methods=["GET", "POST"])
def keep():
    """
    回收站主页，获取回收站里的图片所有信息
    :return: 返回回收站主页html
    """
    pic_li = os.listdir('./static/images_keep/')
    print(pic_li)
    pic_li.sort(reverse=True)
    a = datetime.datetime.now()
    a = a + datetime.timedelta(0.5)
    time_now = datetime.datetime.strftime(a, "%Y-%m-%d")
    context = {'name': "xiaohua", 'li': pic_li, "time": time_now}
    return render_template('home_keep.html', context=context)


@app.route("/clear", methods=["GET", "POST"])
def clear():
    """
    回收站主页，获取回收站里的图片所有信息
    :return: 返回回收站主页html
    """
    pic_li = os.listdir('./static/images_clear/')
    print(pic_li)
    pic_li.sort(reverse=True)
    a = datetime.datetime.now()
    a = a + datetime.timedelta(0.5)
    time_now = datetime.datetime.strftime(a, "%Y-%m-%d")
    context = {'name': "xiaohua", 'li': pic_li, "time": time_now}
    return render_template('home_clear.html', context=context)


@app.route("/clear_all", methods=["GET", "POST"])
def clear_all():
    """
    清空回收站
    :return: 返回回收站主页html
    """
    pic_li = os.listdir('./static/images_delete/')
    for name in pic_li:
        file_name = './static/images_delete/%s' % name
        file_name2 = './static/images_clear/%s' % name
        shutil.move(file_name, file_name2)
    return redirect(url_for("miss"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=520, debug=True)