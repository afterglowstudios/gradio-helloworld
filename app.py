import gradio as gr
import os
import numpy as np
import time
from dotenv import load_dotenv

# load environment variables, if Bashable hosts your model, these will be set automatically
# if you host your model, you can set these values manually
load_dotenv()
GRADIO_SERVER_NAME = os.getenv("GRADIO_SERVER_NAME")
GRADIO_SERVER_PORT = os.getenv("GRADIO_SERVER_PORT")

# process inputs and return outputs
# your code goes in this function.  
def predict(sessionToken, name, input_img):

    start_ts = time.time()

    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()

    stop_ts = time.time()

    # submit results to bashable with the session token
    # {
    #    sessionToken: (string) - required
    #       session token that was passed to your model
    #    cost_per_hr_usd: (float) - required
    #       cost of instance that will be multiplied by duration, 
    #       if bashable hosts your model we will override this value
    #    duration: (float) - required
    #       stop_ts - start_ts
    #    fixed_cost_usd: (float) - optional
    #       additional fixed cost per call of running your model if you have dependencies, 0.0 by dfault
    # }

    gradioResult = [
        f"Hello {name}!", 
        sepia_img, 
        ]
    return gradioResult

# define gradio interface that include input/output text and images
# See https://github.com/gradio-app/gradio for more details
demo = gr.Interface(predict, 
                    inputs=[gr.Textbox(label='sessionToken', visible=False), # sessionToken is automatically pupulated by Bashable
                            gr.Textbox(label='name'), 
                            gr.Image(label='input_image')], 
                    outputs=[gr.Textbox(label='reply'),
                             gr.Image(label='output_image')])

# launch gradio interface with authentication enabled
demo.launch(server_name=GRADIO_SERVER_NAME, server_port=int(GRADIO_SERVER_PORT))