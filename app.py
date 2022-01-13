import base64, secrets, io, os
from PIL import Image, ImageOps
from urllib.request import urlopen

from flask import Flask, request, jsonify, render_template
import numpy as np
import

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import pymysql

model = load_model("./model/model.h5")

app = Flask(__name__)

#Enter here your database informations
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "testingdb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    searchbox = request.form.get("text")
    connection = pymysql.connect()
    cursor = mysql.connection.cursor()
    query = "select * from books where title LIKE '{}%' order by title".format(searchbox)
    cursor.execute(query)
    result = cursor.fetchall()
    return jsonify(result)

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