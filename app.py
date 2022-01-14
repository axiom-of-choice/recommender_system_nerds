import base64, secrets, io, os
from PIL import Image, ImageOps
from urllib.request import urlopen

from flask import Flask, request, jsonify, render_template
import numpy as np
import psycopg2
import psycopg2.extras

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

#model = load_model("./model/model.h5")

app = Flask(__name__)

#Enter here your database informations
DB_HOST = "localhost"
DB_NAME = "books"
DB_USER = "postgres"
DB_PASS = "admin"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route("/fetchrecords",methods=["POST","GET"])
def fetchrecords():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        query = request.form['query']
        #print(query)
        if query == '':
            cur.execute("SELECT * FROM employee ORDER BY id DESC")
            employeelist = cur.fetchall()
            print('all list')
        else:
            search_text = request.form['query']
            print(search_text)
            cur.execute("SELECT * FROM employee WHERE office IN (%s) ORDER BY id DESC", [search_text])
            employeelist = cur.fetchall()
    return jsonify({'htmlresponse': render_template('response.html', employeelist=employeelist)})



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def main():
    miJSON = request.json
    try:
        imagen64 = miJSON["imagen"]
        imgdata = urlopen(imagen64)
        imgdata = imgdata.read()
        imgdata = Image.open(io.BytesIO(imgdata))

        password_length = 13
        extension = "png"
        nomre_unico = f'{secrets.token_urlsafe(password_length)}.{extension}'
        imgdata = imgdata.resize((28, 28))
        imgdata.save(nomre_unico)

        im = image.load_img(nomre_unico, color_mode='grayscale', target_size=(28, 28))
        os.remove(nomre_unico)

        etiqueta = predecir_im(im, invertir=False)
        respuesta = {"etiqueta": etiqueta}

        return jsonify(respuesta)
    except:
        return {"error": "Tuvimos un problema"}


if __name__ == "__main__":
    app.run()


'''def predecir_im(im, invertir=True):
    image = img_to_array(im)
    image.shape

    # Scale the image pixels by 255 (or use a scaler from sklearn here)
    image /= 255

    # Flatten into a 1x28*28 array
    img = image.flatten().reshape(-1, 28 * 28)
    img.shape
    if invertir:
        img = 1 - img

    # plt.imshow(img.reshape(28, 28), cmap=plt.cm.Greys)

    resultado = model.predict(img)
    resultado = np.argmax(resultado, axis=-1)
    return int(resultado[0])'''