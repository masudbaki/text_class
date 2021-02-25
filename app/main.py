from flask import Flask, request
from os.path import dirname, join
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

app= Flask(__name__)
@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1>"


@app.route("/predict", methods=['POST'])
def predict():
  if request.method == 'POST':
    message = request.form['message']
    data = [message]
  filename = "/content/model/tokenizer.pickle"
  with open(filename, 'rb') as handle:
    tokenizer = pickle.load(handle)
  texts = tokenizer.texts_to_sequences(data)
  processed_string = pad_sequences(texts, maxlen=859, padding='post')
    # Load the TFLite model and allocate tensors.
  interpreter = tf.lite.Interpreter(model_path="/content/model/FT_model.tflite")
  interpreter.allocate_tensors()
    # Get input and output tensors.
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()
    # Test the model on random input data.
  input_shape = input_details[0]['shape']
  input_data = np.array(processed_string, dtype=np.float32)
  interpreter.set_tensor(input_details[0]['index'], input_data)
  interpreter.invoke()
  output_data = interpreter.get_tensor(output_details[0]['index'])
  print(output_data[0][0])
  return message
    
  
  return message

