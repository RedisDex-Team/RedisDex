# RedisDex

## Descripción

Tienda online de cartas de pokemon creada con Django y Redis.

Esto es un proyecto para exponer los beneficios de la tecnología Redis en determinadas situaciones.

## Manual de despliegue

1. Instalación de *Redis*: 

Para la instalación de Redis se puede seguir la siguiente guía de instalación: [Install Redis Community Edition](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/)

Si usas windows puedes descargar Redis desde el siguiente enlace: [microsoftarchive/redis](https://github.com/microsoftarchive/redis/releases/tag/win-3.0.504).

2. Instalación de *Python3.12*: 

Instalar Python 3.12 desde la página oficial: [python.org](https://www.python.org/downloads/)


> Los siguientes comandos se deben de ejecutar en la carpeta raíz del proyecto


3. Creación de entorno virtual (opcional):

```bash
python3.12 -m venv venv
```

4. Instalación de las dependencias

```bash
pip3.12 install -r requirements.txt
```

5. Crear las migraciones

```bash
python3.12 manage.py makemigrations
```

6. Realizar las migraciones

```bash
python3.12 manage.py migrate
```

7. Crear entradas de pruebas (opcional)

```bash
python3.12 manage.py seed
```

8. Correr el servidor *Django*:

```bash
python3.12 manage.py runserver
```

9. Ejecución del servidor Redis

Para Linux:
```bash
redis-server .\redis-conf\redis_master.conf
redis-server .\redis-conf\redis_slave.conf
```

Para Windows:
```bash
redis-server.exe .\redis-conf\redis_master.conf
redis-server.exe .\redis-conf\redis_slave.conf
```

10. Acceder al servidor:

Por defecto, el servidor se ejecuta en `http://127.0.0.1:8000/`.

## Credenciales por defecto

- Usuario: `user1`
- Contraseña: `1234`
---
- Usuario: `admin`
- Contraseña: `admin`
