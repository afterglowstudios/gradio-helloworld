import gradio as gr

def echo(sessionID, name, request: gr.Request):
    if request:
        print("Request headers dictionary:", request.headers)
        print("IP address:", request.client.host)
    return sessionID+" "+name, request.headers

io = gr.Interface(echo, 
                  inputs=[gr.Textbox(label='sessionToken', visible=False),
                          gr.Textbox(label='name')], 
                outputs=["textbox",
                         "textarea"]).launch()