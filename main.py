import streamlit as st
from sympy import *

# Interface
st.title("🧮 Sci-Calc : Calculatrice scientifique avec Python")

st.write("## 📌 Guide des symboles et opérations")
st.markdown("""
- **Puissance** : `x**n` (ex: `x**3` pour x³)
- **Multiplication** : `*` (ex: `2*x`)
- **Division** : `/` (ex: `x/2`)
- **Addition** : `+` (ex: `x + 5`)
- **Soustraction** : `-` (ex: `x - 3`)
- **Exponentielle** : `exp(x)` pour e^x
- **Logarithme** : `log(x)`
- **Sinus, Cosinus, Tangente** : `sin(x)`, `cos(x)`, `tan(x)`
""")

# Entrée utilisateur
st.write("## ✍️ Entrez une expression mathématique")
user_input = st.text_input("Expression :", "x**3 + 2*x**2 + x")

# Définition du symbole x
x = symbols('x')

# Vérifier si l'entrée est valide
try:
    expr = sympify(user_input)  # Convertir le texte en expression SymPy
    
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

except Exception as e:
    st.error("⚠️ Erreur dans l'expression. Vérifiez la syntaxe !")
    st.write(e)