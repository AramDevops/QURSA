import time
import streamlit as st
from hydralit import HydraHeadApp
from hydralit_components import HyLoader, Loaders


class MyLoadingApp(HydraHeadApp):

    def __init__(self, title = 'Loader', delay=0,loader=Loaders.standard_loaders, **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.delay = delay
        self._loader = loader

    def run(self,app_target):

        try:
            app_title = ''
            if hasattr(app_target,'title'):
                st.markdown("<img style='width:20%' src='https://i.imgur.com/aHsbSZZ.gif'>", unsafe_allow_html=True)
                app_title = app_target.title

            if app_title == 'Future options 1...':
                with HyLoader():
                    app_target.run()

            elif app_title == 'QURSA':
                app_target.run()
            else:
                app_target.run()



        except Exception as e:
            st.image("./resources/failure.png",width=100,)
            st.error('An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.')
            st.error('Error details: {}'.format(e))

