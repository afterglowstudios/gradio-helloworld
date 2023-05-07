# Gradio-Bashable Hello World
This is a sample gradio app that is configured to allow you to publish on Bashable.art.  Check out 'app.py' for to see the minimal changes needed.

To publish a model on Bashable, and paste the URL this repo in the tool.  After review and testing, your repo will be hosted on our instances and users will be able to run your model. 

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

You must create a .env file with the following contents
``` txt
GRADIO_SERVER_NAME=127.0.0.1
GRADIO_SERVER_PORT=7860
