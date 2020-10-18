# Define la Imagen para Construir
FROM node:12

# Crear directortio para la 'app'
WORKDIR /app

# Copiar package.json en el directorio de la 'app'. Para Node V4 menor usar 'package*.json'
COPY package.json ./

# Instalar Dependencias
RUN npm install

# Copiar todos los archivos en el directorio 'app', excepto los del '.dockerignore'
COPY . .

# Ejecutar 'app' dentro del contenedor
CMD ["npm", "start"]