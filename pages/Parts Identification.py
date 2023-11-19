import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2,preprocess_input as mobilenet_v2_preprocess_input
from streamlit_cropper import st_cropper
from PIL import Image
st.set_option('deprecation.showfileUploaderEncoding', False)

model = tf.keras.models.load_model("saved_model/parts.hdf5")
st.title("EV Vehicle Parts Predictor")
### load file
uploaded_file = st.file_uploader("Choose a image file")

map_dict = {  0:'Controller',
              1:'Battery',
              2:'Invertor',
              3:'Transmission',
              4:'onboardchager',
              5:'ExteriorComponents',
              6:'Elecricmotor',
              7:'CoolingSystem',
              8:'BrakingSystem',
              9:'VehicleInterior'
            }
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Free": None
}
aspect_ratio = aspect_dict[aspect_choice]

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(opencv_image,(224,224))
    # Now do something with the image! For example, let's display it:

    resized = mobilenet_v2_preprocess_input(resized)
    img_reshape = resized[np.newaxis,...]
    img = Image.open(uploaded_file)
    if not realtime_update:
        st.write("Double click to save crop")
    # Get a cropped image from the frontend
    cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                aspect_ratio=aspect_ratio)
    
    # Manipulate cropped image at will
    st.write("Preview")
    _ = cropped_img.thumbnail((150,150))
    st.image(cropped_img)
    # Convert the file to an opencv image.

    Genrate_pred = st.button("Disease")    
    if Genrate_pred:
        prediction = model.predict(img_reshape).argmax()
        # if(map_dict [prediction] == 'turmericfingers'){
        #     Grade = 1
        # }
        st.text(map_dict [prediction])


