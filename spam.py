import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
import numpy as np

# Descargar stopwords en español
nltk.download('stopwords')

# Datos iniciales
mensajes = [
    # SPAM
    "¡Gana dinero rápido desde casa!",
    "Haz clic aquí para reclamar tu premio",
    "Oferta limitada, no te lo pierdas",
    "Crédito inmediato sin verificación",
    "Has sido seleccionado para un regalo exclusivo",
    "Compra ahora y recibe un 50% de descuento",
    "Haz dinero fácil sin esfuerzo",
    "Actualiza tu cuenta bancaria urgentemente",
    "¡Felicitaciones! Has ganado un iPhone",
    "Haz clic para obtener tu recompensa",
    "No pierdas esta oportunidad única",
    "Recibe dinero gratis en minutos",
    "Invierte hoy y duplica tu dinero",
    "Accede a contenido exclusivo ahora",
    "Tu cuenta ha sido bloqueada, verifica tus datos",
    "Transferencia pendiente, confirma tu información",
    "Gana hasta $1000 al día",
    "¡Solo por hoy! Oferta especial",
    "Haz crecer tu negocio en 24 horas",
    "Recibe tu préstamo sin papeleo",

    # NO SPAM
    "Hola, ¿puedes enviarme el informe?",
    "La reunión es mañana a las 10",
    "¿Quieres salir a cenar esta noche?",
    "Adjunto el archivo solicitado",
    "Gracias por tu ayuda con el proyecto",
    "Nos vemos en la oficina a las 9",
    "¿Puedes revisar este documento?",
    "El reporte mensual ya está listo",
    "Confirmo la asistencia al evento",
    "¿Tienes tiempo para una llamada?",
    "Aquí está la presentación que pediste",
    "Feliz cumpleaños, que tengas un gran día",
    "Te envío los datos del cliente",
    "¿Cómo te fue en la entrevista?",
    "Revisé el contrato y está correcto",
    "Nos reunimos en la sala 3",
    "¿Puedes imprimir este documento?",
    "Gracias por tu tiempo",
    "Te llamo en 5 minutos",
    "Buen trabajo con la propuesta"
]

etiquetas = [1]*20 + [0]*20  # 1 = spam, 0 = no spam

# Inicializar vectorizador y modelo
vectorizador = CountVectorizer(stop_words=stopwords.words('spanish'))
X = vectorizador.fit_transform(mensajes)
modelo = MultinomialNB()
modelo.fit(X, etiquetas)

# Función para reentrenar el modelo
def reentrenar_modelo():
    global X, modelo
    X = vectorizador.fit_transform(mensajes)
    modelo.fit(X, etiquetas)
    print("🔁 Modelo reentrenado con los nuevos datos.")

# Función para detectar spam
def detectar_spam(frase):
    entrada = vectorizador.transform([frase])
    prediccion = modelo.predict(entrada)[0]
    prob = modelo.predict_proba(entrada)[0][prediccion]
    if prediccion == 1:
        print(f"⚠️ Esto parece SPAM (confianza: {prob:.2f})")
    else:
        print(f"✅ Esto NO es spam (confianza: {prob:.2f})")

# Menú interactivo
while True:
    print("\n📋 Opciones:")
    print("1. Analizar frase")
    print("2. Agregar nueva frase como SPAM")
    print("3. Agregar nueva frase como NO SPAM")
    print("4. Salir")
    opcion = input("Elige una opción (1-4): ")

    if opcion == "1":
        frase = input("Escribe la frase para analizar:\n> ")
        detectar_spam(frase)

    elif opcion == "2":
        frase = input("Escribe la nueva frase SPAM:\n> ")
        mensajes.append(frase)
        etiquetas.append(1)
        reentrenar_modelo()

    elif opcion == "3":
        frase = input("Escribe la nueva frase NO SPAM:\n> ")
        mensajes.append(frase)
        etiquetas.append(0)
        reentrenar_modelo()

    elif opcion == "4":
        print("👋 ¡Hasta luego!")
        break

    else:
        print("❌ Opción no válida. Intenta de nuevo.")