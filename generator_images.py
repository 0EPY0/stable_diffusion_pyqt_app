import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import keras_cv
from tensorflow import keras

class GenerateImage():
    def __init__(self):
        keras.mixed_precision.set_global_policy("mixed_float16")
        self.model = keras_cv.models.StableDiffusion(img_width=512, img_height=512, jit_compile=True)
        
    def generation(self, prompt, negative_prompt):
        images = self.model.text_to_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            batch_size=1
        )
        return images
