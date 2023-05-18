import os
import streamlit as st
from hydralit import HydraHeadApp


MENU_LAYOUT = [1,1,1,7,2]

class HomeApp(HydraHeadApp):


    def __init__(self, title = 'FOREX AI', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title


    #This one method that must be implemented in order to be used in a Hydralit application.
    #The application must also inherit from the hydrapp class in order to correctly work within Hydralit.
    def run(self):

        try:
            st.markdown("""
                                       <style>

                                       .big-font {
                                           font-size:40px !important;
                                            background: -webkit-radial-gradient(circle, rgba(2,0,36,1) 0%, rgba(210,22,207,1) 49%, rgba(26,210,255,1) 100%);
                                            -webkit-background-clip: text;
                                            -webkit-text-fill-color: transparent;
                                       }
                                       .medium-font {
                                           font-size:25px !important;
                                           color:#EE82EE;
                                           margin-left:45px;
                                       }
                                        .small-font {
                                           font-size:17px !important;
                                           color:#F88379;
                                       }
                                        .formul-font {
                                           color:#00FFFF;
                                       }
                                       .formulff p {
                                            /* other styles goes here... */
                                            display: inline-block;
                                            vertical-align: top;
                                                }
                                       </style>
                                       """, unsafe_allow_html=True)
            st.markdown("<center><img style='margin-top:-250px; width:15%'src='https://media1.giphy.com/media/ZmHLGowrbwbao/giphy.gif?cid=790b7611a263f70a098d2c1ec1deceb45a0029453f089036&rid=giphy.gif&ct=g'></center>",
                    unsafe_allow_html=True)

            spacer = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            st.markdown('<p class="big-font">BUT ET PROBLÉMATIQUE</p>', unsafe_allow_html=True)
            st.write("Bonjour à vous, merci d'avoir consulté l'application QURSA!")

            st.write(f"{spacer} Cette application a de but de résoudre le problème de la complexité de trouver les facteurs premiers d'un entier colossalement grand, (par exemple un nombre composé de 300 chiffres). Tant que le nombre N est grand, tant que le temps pour factoriser ce dernier devient exponentielle. Cependant, la cryptographie moderne joue sur ce point, par exemple le cryptosystème RSA (Rivest-Shamir-Adleman) se base sur cette logique, (on verra avec plus de détaille ce concept dans les parties suivantes).")
            st.write("Il y a différentes manières de factoriser des nombres très grands, habilement avec des algorithmes classiques subexponentiels, comme l'algorithme 'General number field sieve'. Le problème ici, c'est que ces algorithmes ont une certaine limite et ne devient plus pratique si le nombre devient très grand. Par exemple, il faut environ 300 billions d'années à un ordinateur classique pour casser une clef de chiffrement RSA-2048, (un nombre N composé de 617 chiffres), ce qui est énorme, c'est là où on remarque la puissance de la cryptographe asymétrique.")
            st.write("Par contre, il y a une autre méthode ingénieuse et complexe qui va radicalement changer cette perspective et démontre la faiblesse de la sécurité informatique. Cette méthode est nommée le calcul quantique (ordinateur quantique). Les ordinateurs classiques sont basés sur le code binaire (1), (0) afin d'établir des calculs et crée l'information d'une manière digitale. Généralement, l'état du bit peut être soit un 0 ou, soit un 1 avec une probabilité que cela, soit 100 % pour le cas 1 ou 100 % pour le 0. Cependant, l'ordinateur quantique calcule toutes les possibilités à la fois puis nous donne la probabilité que ça, soit davantage un 1 qu'un 0 ou l'inverse. Par exemple, la probabilité de 1 est de 75 % et de 25 % pour le 0. Ce phénomène s'appelle la superposition des qubits et il est propre aux ordinateurs quantiques, alors c'est là où on peut voir la puissance des machines quantiques.")
            st.write("Si on utilise un algorithme polynomial quantique O(log(N)), comme l'algorithme de factorisation Shor sur un ordinateur quantique assez grand, on peut facilement casser le crypto système RSA dans quelques minutes. Ce qui va générer une grande faille de sécurité informatique mondiale, d'une autre façon l'information ne serra plus sécurisée (chiffré) pendant sa migration à une destination quelconque. Donc les informations personnelles seront pratiquement en claire et amplement lisible par un humain. Toutefois, 'un hacker' peux les exploiter pour des raisons malveillantes. Comme récupérer de l'argent depuis les comptes bancaires, ou utiliser des identités illégalement à des fins criminelles, ou même voler des informations top secrètes comme les données des armées et des gouvernements, etc.")



        except Exception as e:
            st.image(os.path.join(".","resources","failure.png"),width=100,)
            st.error('An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.')
            st.error('Error details: {}'.format(e))





