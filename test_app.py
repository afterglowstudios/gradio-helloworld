import unittest
import requests
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import os
from pprint import pprint
import base64
from dotenv import load_dotenv
load_dotenv()

API_INFO_URL_PATH = "/info"
PREDICT_URL_PATH =  "/api/predict"
TIMEOUT = 15
URL = f"http://{os.getenv('GRADIO_SERVER_NAME')}:{os.getenv('GRADIO_SERVER_PORT')}"
SESSION_TOKEN = "dummy_session_token"
SRC_IMG_PATH = 'cat.png'
INPUT_NAME = "Sarah"


# Encode the image to base64 string
def b64encode_image(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    return f"data:image/png;base64,{base64_image}"


# Decode the base64-encoded image
def b64decode_image(base64_image):
    image_data = base64.b64decode(base64_image.split(',')[1])
    return Image.open(BytesIO(image_data))

class MyTest(unittest.TestCase):

    def test_predict(self):
        url = URL

        print(url)

        # get the gradio api labels for we can convert the response into json
        api_info = None
        if api_info is None:
            api_info = requests.get(urljoin(url, API_INFO_URL_PATH), timeout=TIMEOUT).json()
            if 'named_endpoints' not in api_info:
                raise Exception('Request failed', api_info)

        # Set up the gradio input parameters
        payload = {
            "data": [
                SESSION_TOKEN,
                INPUT_NAME,
                b64encode_image(SRC_IMG_PATH),
            ]
        }

        # send the request to the model
        response = requests.post(urljoin(url, PREDICT_URL_PATH),
                                json=payload,
                                timeout=TIMEOUT).json()
        
        # check response
        if 'data' not in response:
            raise Exception('Request failed', response)
                    
        #reformat response into json using gradio output labels
        res = {}
        for value, return_info in zip(response['data'],api_info['named_endpoints']['/predict']['returns']):
            key = return_info['label'].lower()
            if key == 'output_image':
                # load src_img from file
                src_img = Image.open(SRC_IMG_PATH)
                output_img = b64decode_image(value)

                # check image sizes are the same
                self.assertEqual(src_img.size, output_img.size)

                #remove image from print out to avoid spamming the console with image data
                res[key] = '(removed)'
                continue

            res[key] = value
        response['data'] = res
        self.assertTrue(INPUT_NAME in response['data']['reply'])
        self.assertTrue(response['duration'] > 0)
        pprint(response)


if __name__ == '__main__':
    unittest.main()