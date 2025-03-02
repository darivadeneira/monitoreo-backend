# Monitoreo Backend

Este es el backend realizado con Flask para la aplicación web de monitoreo de recursos. Está diseñado específicamente para visualizar y analizar los recursos de máquinas Linux.

## Requisitos

- Python 3.12.2
- pip
- MySQL/MariaDB
- Sistema operativo Linux

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd monitoreo-backend
```

2. Crear un entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
pip install -r requirements-linux.txt
```

3. Configurar la base de datos:
   - Cree un archivo `.env` en la raíz del proyecto con la siguiente estructura:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=monitoreo_db
   DB_PORT=3306
   ```
   - Asegúrese de crear previamente la base de datos especificada en `DB_NAME`

## Ejecución

Para iniciar el servidor backend:

```bash
python run.py
```

El servidor estará disponible en `http://localhost:5000` por defecto.


