import time
import streamlit as st
from hydralit import HydraHeadApp
from hydralit_components import HyLoader, Loaders
import base64

class MyLoadingApp(HydraHeadApp):

    def __init__(self, title = 'Loader', delay=0,loader=Loaders.standard_loaders, **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.delay = delay
        self._loader = loader

    def run(self,app_target):

        try:
            app_title = ''
            if hasattr(app_target, 'title'):
                file_qursa = open("resources/qursa.gif", "rb")
                contents = file_qursa.read()
                data_url = base64.b64encode(contents).decode("utf-8")
                file_qursa.close()

                app_title = app_target.title

            if app_title == 'Home':
                file = open("resources/wd.gif", "rb")
                image = file.read()
                data = base64.b64encode(image).decode("utf-8")
                file.close()

            if app_title == 'Shor Algorithm':
                file = open("resources/VIcR.gif", "rb")
                image = file.read()
                data = base64.b64encode(image).decode("utf-8")
                file.close()

            if app_title == 'RSA Algorithm':
                file = open("resources/boxi.gif", "rb")
                image = file.read()
                data = base64.b64encode(image).decode("utf-8")
                file.close()

            # Create the HTML markup for the images
            image_html = f'''
                
                <div style="display: flex; align-items: center;"><img src="data:image/png;base64,{data_url}" style="height: 25vh;"></div>
                <div style="display: flex; justify-content: center; align-items: center;"><img src="data:image/png;base64,{data}" style="height: 25vh;"></div>
        
            '''

            # Display the images
            st.markdown(image_html, unsafe_allow_html=True)
            app_target.run()


        except Exception as e:
            st.image("./resources/failure.png",width=100,)
            st.error('An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.')
            st.error('Error details: {}'.format(e))

