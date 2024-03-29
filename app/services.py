from tensorflow import keras
# import matplotlib.pyplot as plt
from keras import models
from keras.preprocessing import image
import wget

def gender_classification_pipeline(img_url:str):
    '''
    Takes image url, resize the image, and load it to the gender classifaction model for prediction
    Steps for Training the model can be found at ./models/ 
    '''
    pipeline = models.load_model('./models/gender-classifier.keras')

    try:
        img = wget.download(img_url)
    except Exception as e:
        return f"Problem Downloading Image-{e}", 0.0

    img_np = image.img_to_array(image.load_img(img, target_size=(64,64)))
    test_img = img_np.reshape((1,64,64,3))

    try:
        y = pipeline(test_img/255., training=False)
        out = y.numpy()[0][0]
        output = round(out)
    except Exception as e:
        return f"Issue with output prediction - Change Pipeline code - {e}", 0.0
        
    if output == 0:
        prob = 1-out # probability of predicting output
        img_class = "Female"
    elif output == 1:
        prob = out
        img_class = "Male"
    else:
        return "Issue with output prediction - Change output variable", 0.0 
    
    return img_class, float(prob)

def digit_classification_pipeline(img_url:str):
    '''
    Takes image url, resize the image, and load it to the digit classifaction model for prediction
    Steps for Training the model can be found at ./models/
    '''
    pipeline = models.load_model('./models/digit-classifier.keras')

    try:
        img = wget.download(img_url)
    except Exception as e:  
        return f"Problem Downloading Image-{e}", 0.0

    img_np = image.img_to_array(image.load_img(img, target_size=(28,28)).convert('L'))
    test_img = img_np.reshape((1,28,28,1))

    try:
        y = pipeline(test_img/255., training=False)
        out = y.numpy().argmax(axis=1)[0]
        prob = float(y[0][out])
    except Exception as e:
        # print('Issue with output prediction')
        return f"Issue with output prediction - Change Pipeline code - {e}", 0.0

    img_class = str(out) 
    
    return img_class, float(prob)