"""
@author: Nasr Akram
"""
# imports for the App
from hydralit import HydraHeadApp
from pathlib import Path
import streamlit as st
import base64
import sys

# imports for Quantum part
from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import QFT

#imports for Classical part
from datetime import timedelta
from fractions import Fraction
from sympy import sieve
import pandas as pd
import random
import math
import time


from qiskit import IBMQ

IBMQ.save_account('25ec632a10279f5d4a7deb00aaf8b96f03a5351d0942fd8b3825d13419faf79529d6a1a2032475d437a3dbbfdfb120fc7edd383f7746784f7fab096704f0057e')

#IBMQ.load_account()
#provider = IBMQ.get_provider('ibm-q')
#backend = provider.get_backend('ibmq_qasm_simulator')

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

class CheatApp(HydraHeadApp):

    def __init__(self, title='Shor', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):

        st.markdown("""
            <style>
            .element-container.css-1e5imcs.e1tzin5v1 .css-1v0mbdj.etr89bj1 {
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .element-container.css-1e5imcs.e1tzin5v1 .css-1v0mbdj.etr89bj1 img {
                max-height: 100%;
                width: auto;
                border: 2px solid #fff;
                box-shadow: 10px 10px 5px rgb(38, 255, 4);
                border-radius: 20px;
            }
            </style>""", unsafe_allow_html=True)

        def generate_primes(start, end):
            # Use a sieve algorithm to generate a list of prime numbers in the specified range
            primes = list(sieve.primerange(start, end))
            return primes

        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True

        option = st.sidebar.radio("Choisissez une option :",
                                  ("Insérer le nombre N", "Insérer les nombres premiers P & Q"))

        if option == "Insérer le nombre N":
            st.sidebar.markdown("Entrez le nombre N :")
            number_N = st.sidebar.number_input("N :", key="number_N", min_value=15)
            p, q = None, None

        elif option == "Insérer les nombres premiers P & Q":
            st.sidebar.markdown("Voici des nombres premiers générés aléatoirement avec leurs niveaux de difficulté")
            st.sidebar.write(f"Très facile : {random.sample(generate_primes(300, 700), 3)}")
            st.sidebar.write(f"Facile : {random.sample(generate_primes(3000, 7000), 3)}")
            st.sidebar.write(f"Moyen : {random.sample(generate_primes(30000, 70000), 3)}")
            st.sidebar.write(f"Moyen/Long : {random.sample(generate_primes(300000, 700000), 3)}")

            st.sidebar.markdown("Entrez les nombres premiers P & Q : ")
            p = st.sidebar.number_input("P :", key="number_P", min_value=1, value=3)
            if not is_prime(p):
                st.sidebar.error("P doit être un nombre premier")
            q = st.sidebar.number_input("Q :", key="number_Q", min_value=1,value=5)
            if not is_prime(q):
                st.sidebar.error("Q doit être un nombre premier")

        a_option = st.sidebar.radio("Vous connaisez la valeur de a ? :",
                                    ("Non", "Oui"))
        if a_option == "Oui":
            a_value = st.sidebar.number_input("Valeur de a :", min_value=1, value=7,
                                              key="a_value_user")
        elif a_option == "Non":
            st.sidebar.markdown("La valeur de 'a' va être aléatoire !")

            def value_a(N):
                while True:
                    a = random.randrange(N // 2, N - 1)
                    # Start from N//2 and increment by 2
                    if math.gcd(a, N) == 1:
                        return a

        st.sidebar.markdown("Nombre de Qubits :")
        controll_qubits = st.sidebar.number_input("Qubits de Contrôle :", min_value=2, value=5,
                                                  key="controll_qubits")

        target_qubits = st.sidebar.number_input("Qubits cibles :", min_value=2, value=5,
                                                key="target_qubits")

        fraction_accuracy = st.sidebar.number_input("Precision de la Fraction :", min_value=1, value=20,

                                                  key="fraction_accuracy")
        qpc_option = st.sidebar.radio("Veuillez sélectionner l'option d'exécution : ",
                                      ("Ordinateur quantique (Simulateur)", "Ordinateur quantique"))

        api_val = st.sidebar.text_input("Veuillez insérer votre clé API :")
        if api_val != '':
            IBMQ.save_account(f'{api_val}')
            IBMQ.load_account()
            # Get the provider and backends
            provider = IBMQ.get_provider('ibm-q')
            backends = provider.backends()

            if qpc_option == "Ordinateur quantique (Simulateur)":
                simulators = [backend for backend in backends if backend.configuration().simulator]

                # Dropdown selection for simulator
                simulator_selection = st.sidebar.selectbox(
                    'Sélectionnez un ordinateur:',
                    [f"{sim.name()} (Qubits: {sim.configuration().n_qubits})" for sim in simulators]
                )

                # Get the maximum qubits for the selected simulator
                simulator_max_qubits = next(
                    sim.configuration().n_qubits for sim in simulators if sim.name() == simulator_selection.split(" ")[0]
                )
                pc_name = simulator_selection.split(' ')[0]

                if pc_name ==  "ibmq_qasm_simulator":
                    pc_name = "qasm_simulator"

                backend = Aer.get_backend(pc_name)

                # Display the selected options
                st.sidebar.write(f"Ordinateur: {pc_name}")
                st.sidebar.write(f"Qubits: {simulator_max_qubits}")


            elif qpc_option == "Ordinateur quantique":

                real_quantum_computers = [backend for backend in backends if not backend.configuration().simulator]

                    # Dropdown selection for simulators
                real_qc_selection = st.sidebar.selectbox(
                        'Sélectionnez un ordinateur:',
                        [f"{sim.name()} (Qubits: {sim.configuration().n_qubits})" for sim in real_quantum_computers]
                    )

                    # Get the maximum qubits for the selected simulator
                real_qc_max_qubits = next(
                        sim.configuration().n_qubits for sim in real_quantum_computers if
                        sim.name() == real_qc_selection.split(" ")[0]
                    )

                pc_name = real_qc_selection.split(' ')[0]

                backend = provider.get_backend(pc_name)

                    # Display the selected options
                st.sidebar.write(f"Ordinateur: {pc_name}")
                st.sidebar.write(f"Qubits: {real_qc_max_qubits}")

        # Display the selected or entered number
        st.markdown("Vous avez sélectionné : ")
        if option == "Insérer les nombres premiers P & Q":
            st.write("Votre valeur P : ",p)
            st.write("Votre valeur Q : ", q)
            N = p * q
        else:
           N = number_N

        st.write(f'N : ', N)

        st.write(f'Votre clé publique est : {[N,65537]}')

        message = st.text_input(f"Le message que vous souhaitez chiffrer : ")

        def Crypter(clef_publique, mon_message):
            key, n = clef_publique
            msg_chiffre = [(ord(char) ** key) % n for char in message]
            return msg_chiffre

        msg_ssl = Crypter((65537, N), message)
        st.write(f"Le message chiffré avec la clé publique : {msg_ssl}")

        def initialize_qubits(qc, n, m):
            qc.h(range(n))  # apply hadamard gates
            qc.x(n)

        st.write(f"Fonction: \n\tU(x) = a^x mod {N}")

        def c_modN(a, k):
            U = QuantumCircuit(target_qubits)
            for _ in range(k):
                if a % 2 != 0:
                    for q in range(target_qubits):
                        U.x(q)
            U = U.to_gate()
            U.name = "%i^%i mod N" % (a, k)
            c_U = U.control()
            return c_U

        def modular_exponentiation(qc, n, m, a):
            c_modN_values = [c_modN(a, k) for k in range(n)]  # Precompute c_modN values

            for k, c_modN_value in enumerate(c_modN_values):
                if k > 0:
                    qc.barrier()  # Add a barrier between iterations if needed
                qc.append(c_modN_value, [k] + list(range(n, n + m)))

        def qft_dagger(qc, measurement_qubits):
            qc.append(QFT(len(measurement_qubits),
                          do_swaps=False).inverse(),
                      measurement_qubits)
            qc.name = "QFT†"


        def measure(qc, n):
            qc.measure(n, n)

        def error_correction(qc, n):
            qc.reset(range(n + 2))
            qc.barrier()
            for i in range(n):
                # apply CNOT gates to correct bit flip errors
                qc.cx(i, n)
                qc.cx(i, n + 1)
                qc.cx(i, n + 2)

                qc.x(n)
                qc.x(n + 1)
                qc.x(n + 2)

                qc.cx(i, n)
                qc.cx(i, n + 1)
                qc.cx(i, n + 2)

                qc.x(n)
                qc.x(n + 1)
                qc.x(n + 2)

            qc.barrier()

        def period_finder(n, m, a):
            # set up quantum circuit
            qc = QuantumCircuit(n + m, n)

            # initialize the qubits
            initialize_qubits(qc, n, m)
            qc.barrier()

            # apply modular exponentiation
            modular_exponentiation(qc, n, m, a)
            qc.barrier()

            # apply error correction
            error_correction(qc, n)

            # apply inverse QFT
            qft_dagger(qc, range(n))
            qc.barrier()

            # measure the n measurement qubits
            measure(qc, range(n))
            return qc

        def Modular_multiplicative_inverse(a, n):
            t = 0
            newt = 1
            r = n
            newr = a
            while newr != 0:
                quotient = r // newr
                t, newt = newt, t - quotient * newt
                r, newr = newr, r - quotient * newr
            if r > 1:
                return "a is not invertible"
            if t < 0:
                t = t + n
            return t

        def run_shor():
            start_time = time.time()
            factor_found = False
            attempt = 0
            stop_button = st.button("Arrêter le calcul")
            st.write("Chargement...", end='\t')
            st.write("Connexion à l'ordinateur quantique...", end='\t')
            st.write("Calcul...", end='\t')

            while not factor_found:
                if stop_button:
                    st.write("Calcul arrêté.")
                    sys.exit()
                    break
                try :
                    #n = math.ceil(math.log2(N))
                    #m = n + 1
                    attempt += 1
                    if a_option == "Oui":
                        a = a_value
                    else :
                        a = value_a(N)
                    qc = period_finder(controll_qubits, target_qubits, a)

                    counts = execute(qc, backend=backend).result().get_counts(qc)

                    # convert and add binary periods to list
                    #counts_dec = sorted([int(measured_value[::-1], 2)
                                         #for measured_value in counts])
                    factors = set()
                    target_period = 0

                    # Continuous Fraction Part
                    rows, measured_phases = [], []
                    for output in counts:
                        decimal = int(output, 2)  # convert binary numbers to decimal
                        phase = decimal / (2 ** controll_qubits)  # find eigenvalues
                        measured_phases.append(phase)

                    for phase in measured_phases:
                        frac = Fraction(phase).limit_denominator(fraction_accuracy)
                        rows.append([phase, "%i/%i" % (frac.numerator, frac.denominator), frac.denominator])
                        guesses = [
                            math.gcd(int((a ** int(frac.denominator))) + 1, N),
                            math.gcd(int((a ** int(frac.denominator))) - 1, N)
                        ]

                        for guess in guesses:
                            # Ignore trivial factors
                            if guess != 1 and guess != N and N % guess == 0:
                                factors.add(guess)
                                target_period = int(frac.denominator)
                                factor_found = True

                    df = pd.DataFrame(rows, columns=["Phase", "Fraction", "Guess for r"])
                    #print(df)

                    if len(factors)!=0:
                        r = target_period
                        P = factors.pop()
                        Q = factors.pop() if len(factors) else N // P

                        st.write("Chargement des résultats...")
                        st.write(df)
                        st.write('La valeur de la période "r" est:', {r})
                        st.write('On teste les deux formules pour trouver les facteurs avec:')
                        st.write('N_1 = gcd(', a, '^(', r, '/2) + 1, ', N, ') ')
                        st.write('N_2 = gcd(', a, '^(', r, '/2) - 1, ', N, ') ')
                        if P > 1:
                            st.write(f'Le facteur trouvé avec gcd(', a, '^(', r, '/2) + 1, ', N, ') = ', {P})
                        if Q > 1:
                            st.write(f'Le facteur trouvé avec gcd(', a, '^(', r, '/2) - 1, ', N, ') = ', {Q})

                        st.write("\nTentative %i:" % attempt)
                        st.write(qc.draw(output='mpl'))
                        #print(qc.draw())
                        st.write(plot_histogram(counts))
                        print(counts)

                        st.write("P et Q trouvé avec l'ordinateur quantique : ")
                        st.write('N = ', Q, ' x ', P)

                        phi = (P - 1) * (Q - 1)
                        cle_p = Modular_multiplicative_inverse(65537, phi)
                        st.write("La clé privée trouvée : ")
                        st.write('d = ', cle_p)

                        elapsed_time_secs = time.time() - start_time
                        msg_time = "L'exécution a pris : %s" % timedelta(seconds=round(elapsed_time_secs))
                        st.write(msg_time)
                except Exception as e:
                    st.write(f"An error occurred: {str(e)}")
                    st.write("Arrêt en cours...")
                    break

        if len(msg_ssl)>0:
            if st.button("Démarrer l'algorithme"):
                run_shor()
