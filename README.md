# RedisDex

## Descripción

Tienda online de cartas de pokemon creada con Django y Redis.

Esto es un proyecto para exponer los beneficios de la tecnología Redis en determinadas situaciones.

## Manual de instalación

1. Instalación de *Redis*: [microsoftarchive/redis](https://github.com/microsoftarchive/redis/releases/tag/win-3.0.504)

2. Instalación de *Python3.12*: [python.org](https://www.python.org/downloads/)

3. Creación de entorno virtual (opcional):

```bash
python3.12 -m venv venv
```

4. Instalación de las dependencias

```bash
pip3.12 install -r requirements.txt
```

5. Correr el servidor *Django*:

```bash
python3.12 manage.py runserver
```