# ♻️ Gestión Operativa de Obras y Servicios Públicos

**Sistema de registro, centralización y visualización de información operativa para la Municipalidad de Villa Ojo de Agua.**

Desarrollado en el marco de las Prácticas Profesionalizantes PP1, PP2 y PP3 de la Tecnicatura Superior en Ciencias de Datos e Inteligencia Artificial.

---

## 📌 Descripción del proyecto

El proyecto surge ante la necesidad de mejorar la gestión de la información de la Secretaría de Obras y Servicios Públicos de la Municipalidad de Villa Ojo de Agua.

Anteriormente, los registros relacionados con la recolección de residuos y los accidentes laborales se gestionaban mediante archivos y procedimientos manuales, lo que dificultaba la centralización, el seguimiento y el análisis de los datos.

Como respuesta, se desarrolló una solución digital que integra un chatbot de Telegram, Google Sheets y un dashboard interactivo desarrollado con Python y Streamlit.

El sistema permite registrar información operativa, almacenarla de manera centralizada y visualizarla mediante indicadores y gráficos para facilitar el seguimiento de las actividades y apoyar la toma de decisiones.

## 🎯 Objetivos

- Digitalizar el registro de información operativa.
- Centralizar los datos de recolección de residuos y accidentes laborales.
- Reducir la dependencia de registros manuales.
- Facilitar el acceso y la consulta de información.
- Generar indicadores que contribuyan a la toma de decisiones.
- Mejorar el seguimiento de las actividades de la Secretaría.

## ⚙️ Solución desarrollada

El sistema está compuesto por dos herramientas principales:

### 1. Chatbot de Telegram

Se desarrolló un chatbot que permite a los operadores registrar información mediante una conversación guiada.

Los datos ingresados se almacenan automáticamente en Google Sheets.

Se contemplan dos tipos de registros:

- **Volumen recolectado:** fecha, camión, turno y kilogramos recolectados.
- **Accidentes laborales:** fecha, camión, ruta, turno, barrio, tipo de accidente, lesión y observaciones.

### 2. Dashboard interactivo

Se desarrolló una aplicación web con Streamlit que se conecta a Google Sheets para consultar y visualizar la información registrada.

Entre sus funcionalidades se encuentran:

- Visualización de indicadores generales.
- Consulta de datos de recolección de residuos.
- Análisis de registros por camión y turno.
- Visualización de tendencias temporales.
- Análisis de accidentes laborales.
- Filtros para explorar la información.
- Tablas de consulta de registros.

## 🏗️ Arquitectura del sistema

El funcionamiento general se organiza de la siguiente manera:

1. Los operadores ingresan información mediante el chatbot de Telegram.
2. El chatbot procesa los datos y los registra en Google Sheets.
3. Google Sheets funciona como repositorio centralizado.
4. El dashboard desarrollado en Streamlit consulta los registros.
5. Python, Pandas y Plotly permiten procesar y visualizar la información.

## 🛠️ Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| Python | Lenguaje principal de desarrollo |
| Telegram | Interfaz de registro mediante chatbot |
| Google Sheets | Almacenamiento centralizado |
| Streamlit | Desarrollo del dashboard |
| Pandas | Procesamiento y análisis de datos |
| Plotly | Visualizaciones interactivas |
| gspread | Conexión con Google Sheets |
| Google Auth | Autenticación para acceder a los datos |
| Git y GitHub | Control de versiones y alojamiento del código |

## 📂 Estructura del repositorio

```text
Gestion-Operativa-Obras-Servicios-Publicos/
│
├── app.py
├── probar_conexion.py
├── requirements.txt
├── .gitignore
│
└── chatbot/
    └── Chat_Bot_Telegram.ipynb
```

## 🚀 Instalación y ejecución

### Requisitos previos

- Python instalado.
- Acceso a una cuenta de Google.
- Credenciales de una cuenta de servicio de Google con permisos sobre la hoja de cálculo.
- Acceso a los registros almacenados en Google Sheets.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Annamalag/Gestion-Operativa-Obras-Servicios-Publicos.git
```

### 2. Ingresar al proyecto

```bash
cd Gestion-Operativa-Obras-Servicios-Publicos
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las credenciales

Para ejecutar localmente, colocar el archivo JSON de credenciales en la ubicación esperada por la aplicación.

Para el despliegue en Streamlit Community Cloud, configurar las credenciales de Google Sheets mediante la sección **Secrets**.

No publicar archivos de credenciales, tokens ni claves privadas.

### 5. Ejecutar el dashboard

```bash
streamlit run app.py
```

## 🔐 Seguridad

Las credenciales de acceso a Google Sheets deben mantenerse fuera del repositorio público.

Se utiliza `.gitignore` para excluir archivos sensibles y evitar su publicación accidental.

Las credenciales utilizadas en el entorno de despliegue se configuran mediante Secrets.

## 🔮 Mejoras futuras

Se identifican oportunidades para continuar fortaleciendo el sistema:

- Incorporar autenticación de usuarios mediante usuario y contraseña.
- Implementar diferentes roles y permisos de acceso.
- Mejorar los mecanismos de validación y normalización de datos.
- Incorporar respaldos automáticos.
- Agregar alertas ante situaciones operativas relevantes.
- Ampliar los indicadores y herramientas de análisis.
- Implementar nuevas funcionalidades para facilitar el seguimiento territorial.

Estas mejoras forman parte de las propuestas de evolución del proyecto y no se presentan como funcionalidades ya implementadas.

## 👥 Integrantes

**Tecnicatura Superior en Ciencias de Datos e Inteligencia Artificial**

- Agustina Pieroni
- Tobias Escobedo Miranda
- Ana Laura Malagueño

**Institución beneficiaria:** Municipalidad de Villa Ojo de Agua.

**Área:** Secretaría de Obras y Servicios Públicos.

**Proyecto:** Prácticas Profesionalizantes PP1, PP2 y PP3.

---

## 📄 Licencia

Proyecto académico desarrollado en el marco de las Prácticas Profesionalizantes.