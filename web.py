from flask import Flask, request, send_from_directory, redirect
import os, json, uuid, datetime

app = Flask(__name__)
@app.route('/<path:path>')
def send_file(path): 
    response = send_from_directory(app.static_folder, path)
    if True and 'data' in path: response.cache_control.max_age = 1
    return response

@app.route('/')
def index(): return redirect('/index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # print(request.files)
    # print(request.form)
    print(request.data)
    import base64
    ret = json.loads(request.data.decode('utf-8'))
    data = ret["data"]
    img = base64.b64decode(data.split(",")[-1])
    fn = os.path.join(app.static_folder+'/data/annotations', ret["filename"])
    if os.path.exists(fn):
        os.rename(fn, fn+"."+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    #     # print(imgdata)
    # filename = 'upload/some_image.png'  # I assume you have a way of picking unique filenames
    with open(fn, 'wb') as f:
        f.write(img)
    return 'file uploaded successfully'
        # print(request.get_json())
    # if request.method == 'POST':
    #     f = request.files['file']
    #     fn = os.path.join('upload', f.filename)
    #     if os.path.exists(fn):
    #         os.rename(fn, fn+"."+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    #     f.save(fn)
    #     return 'file uploaded successfully'
    # print('/upload')
    # print(request.method)
    # print(request.files['file'])
    # print(request.form)
    # print(dir(request))
    # data = dict(request.form)
    # print(data)
    # return "OK"
    # if request.method == 'POST':
    #     print(request.files)
    #     file = request.files['file']
    #     extension = os.path.splitext(file.filename)[1]
    #     f_name = str(uuid.uuid4()) + extension
    #     file.save(os.path.join(app.static_folder+'/upload', f_name))
    #     return json.dumps({'filename':f_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
