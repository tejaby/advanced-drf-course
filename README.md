## Requisitos

- Python 3.12.0
- virtualenv (para gestionar las dependencias)

1. Crea un entorno virtual con virtualenv o venv

2. Activa el entorno virtual

- En Windows (cmd):

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

3. Instala las dependencias del proyecto

pip install -r requirements.txt

4. Ejecuta las migraciones

python manage.py makemigrations
python manage.py migrate