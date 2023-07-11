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
from qiskit import QuantumCircuit, Aer, execute, IBMQ
from qiskit.circuit.library import QFT

#imports for Classical part
from datetime import timedelta
from fractions import Fraction
from sympy import sieve
import pandas as pd
import random
import math
import time

import concurrent.futures

import threading

# Shared variable to indicate if a factor is found

# Lock to synchronize access to the shared variable
factor_lock = threading.Lock()
p_q_list = []
a_user = []
factor_stat = []

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
            .css-1v0mbdj.ebxwdo61 {
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .css-1v0mbdj.ebxwdo61 img {
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

        st.sidebar.title(':blue[Paramètres classique] :hammer_and_wrench: :')

        option = st.sidebar.radio("Choisissez une option :",
                                  ("Insérer le nombre N", "Insérer les nombres premiers","Génération aléatoire"))

        if option == "Insérer le nombre N":
            st.sidebar.markdown("Entrez le nombre N :")
            number_N = st.sidebar.text_input("N :", key="number_N")
            N = number_N
            p, q = None, None

        elif option == "Insérer les nombres premiers":
            st.sidebar.markdown("Entrez les nombres premiers :")
            p = st.sidebar.number_input("P :", key="number_P", min_value=1, value=5)
            if not is_prime(p):
                st.sidebar.error("P doit être un nombre premier")
            q = st.sidebar.number_input("Q :", key="number_Q", min_value=1,value=3)
            if not is_prime(q):
                st.sidebar.error("Q doit être un nombre premier")

        elif option == "Génération aléatoire":

            ln = st.sidebar.number_input("Longueur des nombres premiers :", min_value=1, value=2,
                                             key="primes_gen")
            def generator(v_ln):
                range_start = 10 ** (v_ln - 1)
                range_end = 10 ** v_ln
                kl = random.sample(generate_primes(range_start, range_end), 2)
                return kl

            if len(p_q_list) == 0:
                res_kl = generator(ln)
                p_q_list.append(res_kl[0])
                p_q_list.append(res_kl[1])

            if st.sidebar.button("Générer", key="button1"):
                p_q_list.clear()
                res_kl = generator(ln)
                p_q_list.append(res_kl[0])
                p_q_list.append(res_kl[1])

        a_option = st.sidebar.radio("Vous connaisez la valeur de a ? :",
                                    ("Non", "Oui"))
        if a_option == "Oui":
            value_a_input = st.sidebar.number_input("Valeur de a :", min_value=1, value=7,
                                              key="a_value_user")
            a_user.clear()
            a_user.append(value_a_input)

            st.write("La valeur de 'a' est : ",a_user[0])

        elif a_option == "Non":
            a_user.clear()
            st.sidebar.markdown("La valeur de 'a' va être aléatoire !")

        st.sidebar.title('--------------------------------------')

        st.sidebar.title(':violet[Paramètres quantique] :zap: :')


        st.sidebar.markdown("Nombre de Qubits :")
        controll_qubits = st.sidebar.number_input("Qubits de Contrôle :", min_value=2, value=5,
                                                  key="controll_qubits")

        target_qubits = st.sidebar.number_input("Qubits cibles :", min_value=2, value=4,
                                                key="target_qubits")

        st.sidebar.title('--------------------------------------')

        st.sidebar.title(":green[Paramètres d'optimisation] :pushpin: :")

        fraction_accuracy = st.sidebar.number_input("Precision de la Fraction :", min_value=1, value=20,

                                                  key="fraction_accuracy")

        num_instances = st.sidebar.number_input("Processus parallèle :", min_value=1, value=5,

                                                  key="proc_para")

        st.sidebar.title('--------------------------------------')

        st.sidebar.title(":orange[Options d'exécution (facultatif)] :bow_and_arrow: :")

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
                if pc_name == "simulator_statevector":
                    pc_name = "statevector_simulator"

                print(pc_name)
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
        else :
            # Defaults backend
            backend = Aer.get_backend('qasm_simulator')

        # Display the selected or entered number

        if option == "Insérer le nombre N":
            try:
                N = int(N)
            except:
                st.write("Veuillez insérer un entier !")
                st.write("Valeur par défaut du système :")
                N = 15

        elif option == "Génération aléatoire":
            p = p_q_list[0]
            q = p_q_list[1]
            st.write("Votre valeur P : ",p)
            st.write("Votre valeur Q : ", q)
            N = p * q

        else :
            st.write("Votre valeur P : ",p)
            st.write("Votre valeur Q : ", q)
            N = p * q

        st.write(f'N : ', N, '(',len(str(N)),')')

        st.write(f'Votre clé publique est : {[N,65537]}')

        message = st.text_input(f"Le message que vous souhaitez chiffrer : ")

        def Crypter(clef_publique, mon_message):
            key, n = clef_publique
            msg_chiffre = [(ord(char) ** key) % n for char in mon_message]
            return msg_chiffre

        msg_ssl = Crypter((65537, N), message)

        st.write(f"Le message chiffré avec la clé publique : {msg_ssl}")

        def value_a(N):
            while True:
                a = random.randint(2, N - 1)
                # Start from N//2 and increment by 2
                if math.gcd(a, N) == 1:
                    return a

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
            U.name = "%i^%i mod N" % (a, k-1)
            c_U = U.control()
            return c_U

        def modular_exponentiation(qc, n, m, a):
          c_modN_values = [c_modN(a, k-1) for k in range(n)]  # Precompute c_modN values

          for k, c_modN_value in enumerate(c_modN_values):
            if k > 0:
              qc.append(c_modN_value, [k] + list(range(n, n + m)))

        def qft_dagger(qc, measurement_qubits):
            qc.append(QFT(len(measurement_qubits),
                          do_swaps=False).inverse(),
                      measurement_qubits)
            qc.name = "QFT†"


        def measure(qc, n):
            qc.measure(n, n)

        def error_correction(qc, n,m):
            qc.reset(range(n))
            qc.barrier()

            err_control_qubits = range(n)
            err_target_qubits = range(n,n+m-1)  # Assuming 3 target qubits for this example

            for i in err_control_qubits:
                # apply CNOT gates to correct bit flip errors
                for j in err_target_qubits:
                    qc.cx(i, j)
                for j in err_target_qubits:
                    qc.x(j)

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
            error_correction(qc, n, m)
            qc.barrier()
            
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

        r_list, futures, data_counts, list_r_val, rows, measured_phases = [], [], [], [], [], []

        def phase_estimator():
            if len(a_user) > 0:
                a = a_user[0]
            else:
                a = value_a(N)
            qc = period_finder(controll_qubits, target_qubits, a)
            counts = execute(qc, backend=backend).result().get_counts(qc)
            data_counts.append(counts)
            for output in counts:
                decimal = int(output, 2)  # convert binary numbers to decimal
                phase = decimal / (2 ** controll_qubits)  # find eigenvalues
                measured_phases.append(phase)
            for estimated_phase in measured_phases:
                frac = Fraction(estimated_phase).limit_denominator(fraction_accuracy)
                rows.append([phase, "%i/%i" % (frac.numerator, frac.denominator), frac.denominator])
                list_r_val.append(frac.denominator//2)
            for i in list(set(list_r_val)):
                r_list.append(i)
            #st.write(r_list)
        def p_q_finder():
            start_time = time.time()
            attempt = 0
            while len(factor_stat) == 0 :
                if stop_button:
                    st.write("Calcul arrêté.")
                    break
                try:
                    attempt += 1
                    if len(a_user) > 0:
                        n_value_a = a_user[0]
                    else:
                        n_value_a = value_a(N)

                    factors = set()
                    ls_periods = []

                    for r_val in r_list:
                        power_result = pow(n_value_a, r_val)
                        guesses = [
                            math.gcd(power_result + 1, N),
                            math.gcd(power_result - 1, N)
                        ]

                        for guess in guesses:
                            # Ignore trivial factors
                            if guess != 1 and guess != N and N % guess == 0:
                                factors.add(guess)
                                ls_periods.append(r_val)

                        """ 
                         print(tabulate(rows,
                              headers=["Phase", "Fraction", "Guess for r"],
                              colalign=('right', 'right', 'right')))
                        """

                    # Initialize futures as an empty list before the if statement

                    if len(factors) != 0:
                        df = pd.DataFrame(rows, columns=["Phase", "Fraction", "Estimation de 'r'"])
                        factor_stat.append(True)
                        r = ls_periods[0]
                        P = factors.pop()
                        Q = factors.pop() if len(factors) else N // P

                        print("\nTentative %i:" % attempt)

                        st.write("Chargement des résultats...")
                        st.write(df)
                        st.write('La valeur de la période "r" est:', {r})
                        st.write('On teste les deux formules pour trouver les facteurs avec:')
                        st.write('N_1 = gcd(', n_value_a, '^(', r, '/2) + 1, ', N, ') ')
                        st.write('N_2 = gcd(', n_value_a, '^(', r, '/2) - 1, ', N, ') ')

                        st.write(" ")

                        try:
                            v = math.gcd(pow(n_value_a, int(r // 2)) + 1, N)
                            k = math.gcd(pow(n_value_a, int(r // 2)) - 1, N)

                            if v != 1:
                                st.write(f'Le facteur trouvé avec gcd(', n_value_a, '^(', r, '/2) + 1, ', N, ') = ', {v})
                                st.write(f'Le facteur manquant est N //', v, '=', N // v)
                            if k != 1:
                                st.write(f'Le facteur trouvé avec gcd(', a, '^(', r, '/2) - 1, ', N, ') = ', {k})
                                st.write(f'Le facteur manquant est N //', v, '=', N // v)
                        except:
                            print('Aucun facteur trouvé.')


                        l_qc = period_finder(controll_qubits, target_qubits, n_value_a)
                        st.write("\nTentative %i:" % attempt)
                        st.write(l_qc.draw(output='mpl'))
                        st.write(plot_histogram(data_counts))

                        print(data_counts)

                        st.write("P et Q trouvé avec l'ordinateur quantique :")
                        st.write('N = ', Q, ' x ', P)

                        phi = (P - 1) * (Q - 1)
                        cle_p = Modular_multiplicative_inverse(65537, phi)
                        st.write("La clé privée trouvée :")
                        st.write('d = ', cle_p)

                        elapsed_time_secs = time.time() - start_time
                        msg_time = "L'exécution a pris : %s" % timedelta(seconds=round(elapsed_time_secs))
                        st.write(msg_time)

                        break

                except Exception as e:
                    st.write(f"An error occurred: {str(e)}")
                    st.write("Arrêt en cours...")
                    break

        if len(msg_ssl)>0:
            if st.button("Démarrer l'algorithme", key="button3"):
                factor_stat.clear()
                phase_estimator()
                stop_button = st.button("Arrêter le calcul", key="button2")
                st.write("Chargement...", end='\t')
                st.write("Connexion à l'ordinateur quantique...", end='\t')
                st.write("Calcul...", end='\t')
                print("Calcul...", end='\t')
                # Create a ThreadPoolExecutor with the desired number of workers
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_instances)

                # Submit the function multiple times to the executor
                futures = [executor.submit(p_q_finder()) for _ in range(num_instances)]
                concurrent.futures.wait(futures)



