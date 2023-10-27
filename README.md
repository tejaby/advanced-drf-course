# advanced django rest framework course

## Requisitos

- Python 3.12.0
- Django 4.2.6
- Entorno virtual (para gestionar las dependencias)

## Instalación

Crea un entorno virtual con virtualenv o venv

Activa el entorno virtual

- En Windows (cmd):

  ```
  venv\Scripts\activate
  ```

- En Windows (PowerShell):

  ```
  .\venv\Scripts\Activate.ps1
  ```

- En macOS y Linux:

  ```
  source venv/bin/activate
  ```

Instala las dependencias del proyecto

```
pip install -r requirements.txt
```

Ejecuta las migraciones

python manage.py makemigrations
python manage.py migrate

¡Eso es todo, hemos terminado!

```
./manage.py runserver
```
