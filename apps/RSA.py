
"""
@author: Nasr Akram
"""
from streamlit.components.v1 import html
from hydralit import HydraHeadApp
import streamlit as st
from numpy import gcd
import os


class LoaderTestApp(HydraHeadApp):

    def __init__(self, title='RSA Algorithm', delay=0, **kwargs):
        self.__dict__.update(kwargs)
        self.title = title
        self.delay = delay

    def run(self):

        global msg_ssl

        st.markdown("""
                           <style>
                           .big-font {
                               font-size:40px !important;
                                background: -webkit-radial-gradient(circle, rgba(0,36,21,1) 0%, rgba(210,22,207,1) 0%, rgba(255,243,26,1) 100%);
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
                               color:#ff5400;
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

        try:
            if True:
                import rsa
                st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)
                html(
                    "<style>.open-button {  border-radius : 5px ;background-color: #33006F;  color: white;  padding: 16px 20px;  border: none;  cursor: pointer;  opacity: 0.8;  position: fixed;  bottom: 23px;  right: 28px;  width: 280px;}/* The popup form - hidden by default */.form-popup { width: 100%; height:100%; display: none;  position: fixed;  bottom:0;  right: 15px;  border: 1px solid #33006F;  z-index: 9;  border-radius:5px;}/* Add styles to the form container */#myForm{ color: white;  max-width: 600px;  padding: 10px;  background-color: #002147;}/* Set a style for the submit/login button */.form-container .btn {  background-color: #04AA6D;  color: white;  padding: 16px 20px;  border: none;  cursor: pointer;  right:0; top:0; position:fixed; width: 5%;  margin-bottom:10px;  opacity: 0.8;}/* Add a red background color to the cancel button */.form-container .cancel { border-radius: 15px 50px 30px; background-color: #FF003F;}/* Add some hover effects to buttons */.form-container .btn:hover, .open-button:hover {  opacity: 1;}</style><body><button class='open-button' onclick='openForm()'>Ouvrir le Guide des Options</button><div class='form-popup' id='myForm'>  <div action='/action_page.php' class='form-container'>    <h3>QURSA Guide</h3>    <p>Vous pouvez interagir avec l'application, chaque élément dans la documentation ayant un signe ★ peux être manipulé depuis le menu à votre gauche.</p>            <p>Vous pouvez voir que chaque titre est attribué a une option, l'application fonctionne d'une manière intuitive et facile à manipuler.</p>    <br>    <button type='button' class='btn cancel' onclick='closeForm()'>X</button>  </div></div><script>function openForm() {  document.getElementById('myForm').style.display = 'block';}function closeForm() {  document.getElementById('myForm').style.display = 'none';}</script></body></html>")

                RSAmin_val = 17
                with st.sidebar:

                    st.markdown(
                        "<a style='text-decoration: none; color:#ff5400' href='#prime'>★ Les nombres premiers : </a>",
                        unsafe_allow_html=True)

                    z = 1000
                    lower_value = int(
                        st.number_input("Veuillez saisir la valeur de la plage la plus basse: ", min_value=1,
                                        max_value=z,
                                        value=1,
                                        step=1))
                    upper_value = int(
                        st.number_input("Veuillez saisir la valeur supérieure de la plage:  ", min_value=1,
                                        max_value=z,
                                        value=20,
                                        step=1))
                    st.write(" ")
                    st.markdown(
                        "<a style='text-decoration: none; color:#ff5400' href='#keygenauto'>★ Veuillez saisir la taille de votre clef :</a>",
                        unsafe_allow_html=True)

                    st.write("Générateur automatique")

                    rsa_size = st.number_input("La valeur de bit doit être entre 16 et 2048 :", min_value=RSAmin_val,
                                               max_value=2048, value=RSAmin_val,
                                               step=2)
                    st.write(" ")

                    st.markdown(
                        "<a style='text-decoration: none; color:#ff5400' href='#keygenmanu'>★ Veuillez saisir les valeur Q et P :</a>",
                        unsafe_allow_html=True)
                    st.write("Générateur manuelle")

                    P_manuelle = st.number_input("P (doit être un nombre premier) : ", min_value=2,
                                                 max_value=100000,
                                                 value=647,
                                                 step=1)

                    Q_manuelle = st.number_input("Q (doit être un nombre premier) : ", min_value=2,
                                                 max_value=100000,
                                                 value=1061,
                                                 step=1)

                if rsa_size < RSAmin_val:
                    st.write(
                        'for security reasons, the RSA Key Size is to small for a good data protection pick a size between 16 - 2048')
                else:

                    st.markdown('<p class="big-font"> I - VUE GÉNÉRALE DU CRYPTOSYSTEME RSA </p>',
                                unsafe_allow_html=True)
                    st.markdown('<p class="medium-font">1.1 - Introduction :</p>',
                                unsafe_allow_html=True)
                    st.write(
                        "L'algorithme de chiffrement Rivest-Shamir-Adleman (RSA) est un algorithme de chiffrement asymétrique utilisé mondialement par les entreprises multinationales, les gouvernements, les armées et considéré comme la base de la sécurité sur le net (https), Le chiffrement asymétrique utilise une paire de clefs mathématiquement liée pour chiffrer et déchiffrer les données. Une clef privée et une clef publique sont crées, la clef publique étant accessible à tous et la clef privée étant un secret connu uniquement par le créateur de la paire de clefs.")

                    st.write(
                        "Remarque : L'algorithme RSA est une exponentiation populaire dans un corps fini sur des nombres entiers, y compris des nombres premiers, les nombres entiers utilisés par ce cryptosystème sont suffisamment grands, ce qui la rend difficile à résoudre.")
                    st.write(" ")

                    st.markdown("<p class='medium-font'>1.2 - Génération d'une clef RSA  :</p>",
                                unsafe_allow_html=True)
                    st.write("1 - La procédure initiale commence par la sélection de deux nombres premiers p et q, puis calculer leur produit N = pq")
                    with st.echo():
                        Q = 389
                        P = 383
                        N = P * Q
                    st.write('N est le module pour la clef publique et la clef privée')

                    if lower_value > upper_value:
                        st.write(
                            "La valeur de la plage la plus basse doit être inférieure à la valeur de la plage supérieure : ")
                    else:
                        st.markdown("<div id='prime'></div>", unsafe_allow_html=True)
                        st.markdown(
                            f"<p class='small-font'>★ Les nombres premiers dans l'intervalle {lower_value} et {upper_value} sont: </p> ",
                            unsafe_allow_html=True
                        )
                        for number in range(lower_value, upper_value + 1):
                            if number > 1:
                                for i in range(2, number):
                                    if (number % i) == 0:
                                        break

                                else:
                                    st.markdown(f'<table style="width:100%"><tr><td>{number}</td></tr></table>',
                                                unsafe_allow_html=True
                                                )

                    st.write(" ")
                    st.markdown(
                        '<div class="formulff"> <p> 2 - Calculer le totient (phi) : </p> <p class="formul-font"> ϕ(n) = (p−1)(q−1) </p> </div>',
                        unsafe_allow_html=True)

                    st.markdown(
                        "<div class='formulff'> <p> 3 - Choisir un entier e tel que </p> <p class='formul-font'> 1 < e < ϕ(n)</p> <p>, et e premier à ϕ(n) c'est-à-dire : e et ϕ(n) ne partagent aucun facteur autre que 1;</p> <p class='formul-font'> pgcd(e ,ϕ(n) = 1. </p>  </div> ",
                        unsafe_allow_html=True)
                    st.write(
                        "La clef publique est partagée ouvertement, donc tout le monde peut la voir, il n'est pas si important que e soit un nombre aléatoire. En pratique, e est généralement fixé à 65 537.")
                    with st.echo():
                        phi = (P - 1) * (Q - 1)  # 148216
                        e = 65537
                        # 1 < 65537 < ϕ(n)
                        if gcd(e, phi) == 1 and e < phi:
                            print(True)
                        else:
                            print(False)

                    st.write("Remarque : e est publié comme exposant de la clef publique")
                    st.markdown(
                        "<div class='formulff'> <p> Donc notre clef publique dans ce cas est </p> <p class='formul-font'> (N,e) = (148987,65537)</p>",
                        unsafe_allow_html=True)

                    st.markdown(
                        "<div class='formulff'> <p> 4 - Calculer d pour satisfaire la relation de congruence </p> <p class='formul-font'> ed (modϕ(n) = 1) </p> <p>soit </p> <p class='formul-font'>ed = 1+kϕ(n) </p> <p> pour un entier k, </p> <p> On peux simplement dire :</p> <p class='formul-font'> d = 1+kϕ(n)/e </p> </div> ",
                        unsafe_allow_html=True)
                    st.markdown("<p class='formul-font'> Exemple : </p>", unsafe_allow_html=True)
                    st.write("65537 x d (mod 148216) = 1")
                    st.write("65537 x 4401 (mod 148216) = 1")
                    with st.echo():
                        def Modular_multiplicative_inverse(exposant, totient):
                            for k in range(1, totient):
                                if (((exposant % totient) * (k % totient)) % totient == 1):
                                    return k

                        D = Modular_multiplicative_inverse(e, phi)  # 4401

                    st.write("Remarque : d est conservé comme exposant de la clef privée")
                    st.markdown(
                        "<div class='formulff'> <p> Donc notre clef privée dans ce cas est </p> <p class='formul-font'> (N,d) = (148987,4401)</p>",
                        unsafe_allow_html=True)
                    st.write(" ")
                    st.markdown("<p class='medium-font'>1.3 - Chiffrement et déchiffrement :</p>",
                                unsafe_allow_html=True
                                )
                    st.write("1 - Cryptage des messages :")

                    st.markdown(
                        "<div class='formulff'> <p> Afin de crypter les messages, on utilise la formule </p> <p class='formul-font'> c = m^e(mod N) </p>, la valeur m est le message qu'on veut Crypter.</p> </div> ",
                        unsafe_allow_html=True)
                    with st.echo():
                        def Crypter(clef_publique, mon_message):
                            key, n = clef_publique
                            msg_chiffré = [(ord(char) ** key) % n for char in message]
                            return msg_chiffré

                    message = st.text_input(f"Le message que vous souhaitez chiffrer :")

                    st.write("Votre message après le chiffrement avec la clef publique (148987,65537) : ")
                    msg_ssl = Crypter((65537, 148987), message)
                    st.write(msg_ssl)

                    st.write("2 - Décryptage des messages :")

                    st.markdown(
                        "<div class='formulff'> <p> Pour Décrypter le messages crypté, on utilise la formule </p> <p class='formul-font'> m = c^d(mod N). </p></div> ",
                        unsafe_allow_html=True)
                    with st.echo():
                        def Décrypter(clef_privé, mon_message_crypté):
                            key, n = clef_privé
                            msg_déchiffré = [chr((char ** key) % n) for char in mon_message_crypté]
                            return ''.join(msg_déchiffré)

                    st.markdown(
                        f"<div class='formulff'> <p> Le message après le déchiffrement du code QR sachant la clef privée :  </p> <p class='formul-font'> {Décrypter((4401, N), Crypter((65537, 148987), message))}</p></div> ",
                        unsafe_allow_html=True)

                    st.markdown('<p class="medium-font">1.4 - Générateur de clef RSA aléatoire et manuelle </p>',
                                unsafe_allow_html=True)
                    basbits = 1024
                    basdigits = 308
                    st.markdown("<div id='keygenauto'></div>", unsafe_allow_html=True)

                    st.write("1 - Générateur aléatoire : ")
                    st.markdown(
                        f"<p class='small-font'>★ Vous pouvez générer une clef RSA de la taille de votre choix [16 - 2048] bit : </p> ",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='formulff'><p>Votre clef publique est composée d'environ </p> <p class='formul-font'> {int((rsa_size * basdigits) / basbits)}</p> <p> chiffres.</p> </div> ",
                        unsafe_allow_html=True
                    )
                    publicKey, privateKey = (rsa.newkeys(rsa_size))
                    st.write(f'Ceci est la clef publique RSA, Taille({rsa_size}) : (N,e)')

                    st.write("N =", publicKey.n)
                    st.write("e =", publicKey.e)

                    st.write(f'Ceci est la clef privée RSA, Taille({rsa_size}) : (d)')

                    st.write("d =", privateKey.d)

                    st.write('Ceci est les deux nombres premiers p et q :')

                    st.write("p =", privateKey.p)
                    st.write("q =", privateKey.q)

                    st.markdown("<div id='keygenmanu'></div>", unsafe_allow_html=True)

                    st.write("2 - Générateur manuelle : ")

                    st.markdown(
                        f"<p class='small-font'>★ Afin de générer une clef RSA manuellement, P et Q doivent être des nombres premiers (veuillez consulter l'option ★ Les nombres premiers pour facilité votre choix)  : </p> ",
                        unsafe_allow_html=True)

                    if not Q_manuelle and P_manuelle:
                        st.write("")

                    else:
                        N_custom = Q_manuelle * P_manuelle

                        E_custom = 65537

                        phi_custom = (P_manuelle - 1) * (Q_manuelle - 1)

                        st.markdown(
                            f"<div class='formulff'><p>Le module de votre clef publique, N = </p> <p class='formul-font'>{N_custom} </p> </div> ",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<div class='formulff'><p>L'exposant de votre clef publique (par défaut), e = </p> <p class='formul-font'>{E_custom} </p> </div> ",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<div class='formulff'><p>Voici votre clef publique (N,e) = </p> <p class='formul-font'>({N_custom},{E_custom}) </p> </div> ",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<div class='formulff'><p>Voici votre clef privé en utilisant l'inverse multiplicatif modulaire (N,d) = </p> <p class='formul-font'>({N_custom},{Modular_multiplicative_inverse(E_custom, phi_custom)}) </p> </div> ",
                            unsafe_allow_html=True
                        )

            # st.write(
            # f'<iframe width="100%" height="750px" src="https://www.forex.com/en/market-analysis/latest-research/"></iframe>',
            # unsafe_allow_html=True,
            # )
            st.markdown(
                "<a style=' position:fixed; right:5px; bottom:20px; z-index:999; color:red'  href='#linkto_top'><h1>▲</h1></a>",
                unsafe_allow_html=True)
        except Exception as e:
            st.image(os.path.join(".", "resources", "failure.png"), width=100, )
            st.error(
                'An error has occurred...')
            st.error('Error details: {}'.format(e))

