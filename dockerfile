# Usar la imagen oficial de MySQL
FROM mysql:latest

# Configurar las credenciales de la base de datos
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=monitoreo
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=adminpass

# Exponer el puerto de MySQL
EXPOSE 3306
