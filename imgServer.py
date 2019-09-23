import sys,os,re,flask,random

imgDir = "/data_big/meitulu/MeituluCrawler/imgs_old"

app = flask.Flask(__name__)

@app.route('/')
def newone():
    imgFile = os.path.join(imgDir, 'gids')
    imgList = open(imgFile, 'r').readlines()
    imgList = [g.strip().strip('./') for g in imgList]

    gid = imgList[random.randint(0,20)]

    return flask.redirect('/%s' % gid)

@app.route('/<gid>')
def girlPage(gid):
    imgs = []

    for (dirPath, dirName, fileNames) in os.walk(os.path.join(imgDir, gid)):
        for f in fileNames:
            if f.endswith('jpg'):
                imgs.append("%s/%s" % (gid, f))

    return flask.render_template('meinv.html', imgSrc=imgs)

@app.route('/imgs/<gid>/<file>')
def readImg(gid, file):
    with open(os.path.join(imgDir,"%s/%s" % (gid, file)), "rb") as f:
        imgData = f.read()
        resp = flask.Response(imgData, mimetype="image/jpeg")

    return resp

@app.route('/hello/<user>')
def hello_name(user):
   return flask.render_template('meinv.html', name = user)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)