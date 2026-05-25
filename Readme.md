# Segundo Parcial Backend

Este es el proyecto para el segundo parcial de Backend. Está construido utilizando **FastAPI**, **SQLAlchemy** y **PostgreSQL**.

## 🚀 Primeros Pasos

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### 1. Requisitos previos
- Tener Python 3.8 o superior instalado.
- Tener un servidor de base de datos PostgreSQL en funcionamiento.

### 2. Instalar dependencias
Abre tu terminal en la carpeta raíz del proyecto y ejecuta el siguiente comando para instalar las librerías necesarias:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2 python-dotenv pydantic
```
*(Nota: Si tienes problemas instalando `psycopg2`, puedes probar con `pip install psycopg2-binary`)*

### 3. Configurar variables de entorno
El proyecto requiere conectarse a una base de datos PostgreSQL.
1. Crea un archivo llamado `.env` en la raíz del proyecto. Puedes copiar el contenido del archivo `.env.example`.
2. Completa el archivo `.env` con las credenciales de tu base de datos:
```env
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tu_base_de_datos
```
*Nota: Si las tablas no existen, SQLAlchemy se encargará de crearlas automáticamente al iniciar la aplicación.*

### 4. Ejecutar el servidor
Una vez instaladas las dependencias y configurada la base de datos, puedes levantar el servidor de desarrollo ejecutando:
```bash
uvicorn main:app --reload
```
La API estará disponible en `http://localhost:8000`. Puedes acceder a la documentación interactiva autogenerada (Swagger UI) ingresando a `http://localhost:8000/docs` desde tu navegador.


## 📮 Importar Colección de Postman

El proyecto incluye un archivo JSON con la colección de Postman (`Backend_P2.postman_collection.json`) que contiene ejemplos preconfigurados de todas las peticiones a la API (CRUD de Vehículos, Calles, Estacionamientos, etc.) para facilitar sus pruebas.

Para importarla en Postman, sigue estos pasos:

1. Abre la aplicación de **Postman**.
2. En la barra lateral o en la parte superior izquierda, haz clic en el botón **"Import"** (Importar).
3. Aparecerá una ventana emergente. Puedes arrastrar y soltar el archivo directamente ahí, o seleccionar la opción **"File"** (o "choose files").
4. Navega hasta la carpeta de este proyecto y selecciona el archivo `Backend_P2.postman_collection.json`.
5. Confirma haciendo clic en **"Import"**.
6. ¡Listo! Ahora verás la colección importada en tu espacio de trabajo y podrás ejecutar las peticiones contra el servidor local.
