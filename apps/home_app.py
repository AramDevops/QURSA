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
            st.markdown('<p class="big-font">BUTE ET PROBL??MATIQUE</p>', unsafe_allow_html=True)
            st.write("Bonjour ?? vous, merci d'avoir consult?? l'application QURSA!")

            st.write(f"{spacer} Cette application a de bute de r??soudre le probl??me de la complexit?? de trouver les facteurs premiers d'un entier colossalement grand, (par exemple un nombre compos?? de 300 chiffres). Tant que le nombre N est grand, tant que le temps pour factoriser ce dernier devient exponentielle. Cependant, la cryptographie moderne joue sur ce point, par exemple le cryptosyst??me RSA (Rivest-Shamir-Adleman) se base sur cette logique, (on verra avec plus de d??taille ce concept dans les parties suivantes).")
            st.write("Il y a diff??rentes mani??res de factoriser des nombres tr??s grands, habilement avec des algorithmes classiques subexponentiels, comme l'algorithme 'General number field sieve'. Le probl??me ici, c'est que ces algorithmes ont une certaine limite et ne devient plus pratique si le nombre devient tr??s grand. Par exemple, il faut environ 300 billions d'ann??es ?? un ordinateur classique pour casser une clef de chiffrement RSA-2048, (un nombre N compos?? de 617 chiffres), ce qui est ??norme, c'est l?? o?? on remarque la puissance de la cryptographe asym??trique.")
            st.write("Par contre, il y a une autre m??thode ing??nieuse et complexe qui va radicalement changer cette perspective et d??montre la faiblesse de la s??curit?? informatique. Cette m??thode est nomm??e le calcul quantique (ordinateur quantique). Les ordinateurs classiques sont bas??s sur le code binaire (1), (0) afin d'??tablir des calculs et cr??e l'information d'une mani??re digitale. G??n??ralement, l'??tat du bit peut ??tre soit un 0 ou, soit un 1 avec une probabilit?? que cela, soit 100???% pour le cas 1 ou 100???% pour le 0. Cependant, l'ordinateur quantique calcule toutes les possibilit??s ?? la fois puis nous donne la probabilit?? que ??a, soit davantage un 1 qu'un 0 ou l'inverse. Par exemple, la probabilit?? de 1 est de 75???% et de 25???% pour le 0. Ce ph??nom??ne s'appelle la superposition des qubits et il est propre aux ordinateurs quantiques, alors c'est l?? o?? on peut voir la puissance des machines quantiques.")
            st.write("Si on utilise un algorithme polynomial quantique O(log(N)), comme l'algorithme de factorisation Shor sur un ordinateur quantique assez grand, on peut facilement casser le crypto syst??me RSA dans quelques minutes. Ce qui va g??n??rer une grande faille de s??curit?? informatique mondiale, d'une autre fa??on l'information ne serra plus s??curis??e (chiffr??) pendant sa migration ?? une destination quelconque. Donc les informations personnelles seront pratiquement en claire et amplement lisible par un humain. Toutefois, 'un hacker' peux les exploiter pour des raisons malveillantes. Comme r??cup??rer de l'argent depuis les comptes bancaires, ou utiliser des identit??s ill??galement ?? des fins criminelles, ou m??me voler des informations top secr??tes comme les donn??es des arm??es et des gouvernements, etc.")



        except Exception as e:
            st.image(os.path.join(".","resources","failure.png"),width=100,)
            st.error('An error has occurred, someone will be punished for your inconvenience, we humbly request you try again.')
            st.error('Error details: {}'.format(e))





