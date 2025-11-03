import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# Capturar datos de 5 personas
datos = []
for i in range(5):
    print(f"Persona {i+1}:")
    peso = float(input("  Ingresa el peso (kg): "))
    altura = float(input("  Ingresa la altura (m): "))
    datos.append([peso, altura])

# Convertir a array para procesamiento
import numpy as np
X = np.array(datos)

# Escalar los datos con scikit-learn
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("\nDatos normalizados:")
print(X_scaled)
