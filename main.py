import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, diff, integrate, latex, lambdify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import google.generativeai as genai
import os 
load_dotenv()




apkikey = os.getenv("GOOGLE_API_KEY")
# Clé API Gemini (ajoute ta clé ici)
genai.configure(api_key=apkikey)

# Interface Streamlit
st.title("📚 Sci-Calc : Révolutionner l'éducation avec l'IA 🇨🇮")

st.write("## ✍️ Entrez une expression mathématique")
user_input = st.text_input("Expression :", "x**3 + 2*x**2 + x")

# Définition du symbole x
x = symbols('x')

# Vérifier si l'entrée est valide
try:
    expr = sympify(user_input)  # Convertir l'entrée en expression SymPy
    
    # Calculer la dérivée et l'intégrale
    derivative = diff(expr, x)
    integral = integrate(expr, x)

    # Affichage des résultats en LaTeX
    st.write("### 📌 Expression saisie :")
    st.latex(latex(expr))

    st.write("### 🔹 Dérivée :")
    st.latex(latex(derivative))

    st.write("### 🔹 Intégrale :")
    st.latex(latex(integral))

    
    
    # 🔥 Ajout de la démonstration avec LangChain et Gemini
    st.write("### 🧠 Explication détaillée des calculs")
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=apkikey)

    prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Tu es un professeur de mathématiques qui explique à un élève débutant. "
        "Décompose l’explication en plusieurs étapes pédagogiques et utilise des analogies si nécessaire. "
        "Prends un ton bienveillant et clair, en expliquant d'abord le **concept mathématique** avant de montrer les calculs. "
        "Utilise LaTeX pour formater les formules et la reponse doit etre en bloc pas sous une seule ligne fait plusieurs paragraphes, mais garde des explications textuelles accessibles."
    ),
    (
        "human",
        "Peux-tu m’expliquer en détail comment dériver et intégrer cette expression mathématique : {expression} ? "
        "Décompose en **plusieurs étapes conceptuelles** avec une approche progressive."
    )
])
    st.write("Réponse du Modèle:")

    with st.spinner("Génération de la réponse..."):  # ✅ Ajout des parenthèses
        yo = llm.invoke(prompt.format(expression=user_input))  # ✅ Appel correct de Langchain

    st.success("Done!")  # ✅ Succès après exécution

    response = yo  # ✅ Stockage de la réponse

    
    # Affichage de la démonstration
    st.markdown(response.content)
    # Création de la plage de valeurs pour le tracé
    x_vals = np.linspace(-10, 10, 400)
    
    # Convertir l'expression SymPy en fonction utilisable par NumPy
    f = lambdify(x, expr, 'numpy')
    f_prime = lambdify(x, derivative, 'numpy')
    f_integral = lambdify(x, integral, 'numpy')

    # Tracer la courbe
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, f(x_vals), label=f"$f(x) = {latex(expr)}$", color="blue", linewidth=2)
    ax.plot(x_vals, f_prime(x_vals), label=f"$f'(x) = {latex(derivative)}$", linestyle="dashed", color="red")
    ax.plot(x_vals, f_integral(x_vals), label=f"$\\int f(x)dx = {latex(integral)}$", linestyle="dotted", color="green")

    # Personnalisation du graphe
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    
    # Affichage du graphe dans Streamlit
    st.pyplot(fig)

    

except Exception as e:
    st.error("⚠️ Erreur dans l'expression. Vérifiez la syntaxe !")
    st.write(e)
