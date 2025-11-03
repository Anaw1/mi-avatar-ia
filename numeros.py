import tensorflow as tf
import numpy as np

# Datos de entrenamiento
X = np.array([[i] for i in range(1, 101)], dtype=np.float32)
y = np.array([[0] if i % 2 == 0 else [1] for i in range(1, 101)], dtype=np.float32)  # 0 = par, 1 = impar

# Crear modelo
modelo = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
modelo.fit(X, y, epochs=100, verbose=0)

# Input interactivo
while True:
    entrada = input("--------------\nhola! <3 \n--------------\n Escribe un número (o 'salir' para terminar)\n ➡️: ").strip() 
    if entrada.lower() == "salir":
        break
    try:
        numero = int(entrada)

        if not numero.is_integer():
            print("ℹ️ Ingresaste un número real! vuelve a ingresar otro número \n______________")
            continue

        numero_entero = int(numero)
        pred = modelo.predict(np.array([[numero_entero]], dtype=np.float32))[0][0]
        resultado = "par" if pred < 0.5 else "impar"
        print(f"🔢 El número {numero_entero} es {resultado}. (confianza: {pred:.2f})")

    except Exception as e:
        print(f"❌ Eso no parece un número válido. Error: {e}")