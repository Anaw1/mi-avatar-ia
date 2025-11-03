# 🎮 Juego: Adivina el animal con IA (Scikit-learn + TensorFlow)
# Autor: Ana & ChatGPT 💖

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from tensorflow import keras

# -----------------------------
# 1️⃣ Datos iniciales de animales
# -----------------------------
animales = ["Perro", "Gato", "Pez", "Pájaro", "Serpiente", "Elefante"]
# Características:
# [tiene_patas, vuela, vive_en_agua, tiene_pelaje]
caracteristicas = np.array([
    [1, 0, 0, 1],  # Perro
    [1, 0, 0, 1],  # Gato
    [0, 0, 1, 0],  # Pez
    [1, 1, 0, 0],  # Pájaro
    [0, 0, 0, 0],  # Serpiente
    [1, 0, 0, 0],  # Elefante
])

# -----------------------------
# 2️⃣ Entrenar modelo Scikit-learn
# -----------------------------
modelo_sklearn = DecisionTreeClassifier()
modelo_sklearn.fit(caracteristicas, animales)

# -----------------------------
# 3️⃣ Entrenar modelo TensorFlow
# -----------------------------
modelo_tf = keras.Sequential([
    keras.layers.Dense(8, input_shape=(4,), activation='relu'),
    keras.layers.Dense(6, activation='softmax')
])
modelo_tf.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Convertimos las etiquetas de texto a números
mapa_animales = {nombre: i for i, nombre in enumerate(animales)}
y_entrenamiento = np.array([mapa_animales[a] for a in animales])

# Entrenamos la red neuronal
modelo_tf.fit(caracteristicas, y_entrenamiento, epochs=100, verbose=0)

# -----------------------------
# 4️⃣ Juego interactivo
# -----------------------------
print("🎮 ¡Bienvenida al juego Adivina el Animal con IA! 🐾")
print("Responde con 's' para sí o 'n' para no.\n")

preguntas = [
    "¿Tiene patas?",
    "¿Vuela?",
    "¿Vive en el agua?",
    "¿Tiene pelaje?"
]

respuestas = []
for pregunta in preguntas:
    while True:
        r = input(pregunta + " (s/n): ").strip().lower()
        if r in ["s", "n"]:
            respuestas.append(1 if r == "s" else 0)
            break
        else:
            print("Responde solo con 's' o 'n' por favor 😊")

respuestas_np = np.array(respuestas).reshape(1, -1)

# -----------------------------
# 5️⃣ Predicciones de ambas IA
# -----------------------------
pred_sklearn = modelo_sklearn.predict(respuestas_np)[0]

pred_tf_probs = modelo_tf.predict(respuestas_np)
pred_tf_idx = np.argmax(pred_tf_probs)
pred_tf = animales[pred_tf_idx]

print("\n✨ Resultados de las IA ✨")
print(f"🤖 Scikit-learn cree que es: {pred_sklearn}")
print(f"🧠 TensorFlow cree que es: {pred_tf}")

print("\n¿Adivinaron bien? 😸 Si no, puedes volver a jugar y enseñarles más ejemplos para que aprendan mejor.")
