from flask import Flask, render_template, request, redirect
from utils import predict
import config
import utils
import os

app = Flask(__name__)

app.config["UPLOAD_PATH"] = config.UPLOAD_PATH

@app.route('/', methods=['GET', 'POST'])
def index():
      if request.method == 'POST':
            audio_data = request.files['audio']
            print(audio_data)

            save_name = os.path.join(app.config["UPLOAD_PATH"], audio_data.filename)
            audio_data.save(save_name)

            filename, ext = os.path.splitext(save_name)
            if ext == '.mp3':
                  utils.convert_mp3_to_wave(save_name,save_name)

            pred = predict(save_name)
            print(pred)

            return render_template(config.PREDICT_HTML_PATH, prediction=pred) 


      elif request.method == 'GET':
            return render_template(config.HTML_PATH)
      else:
            print('CURD operation not Permitted')


if __name__ == '__main__':
      app.run(debug=True)