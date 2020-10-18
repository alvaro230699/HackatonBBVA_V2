# HackatonBBVA


### Requerimientos

- Permitir archivos con extension: jpg, jpeg, png, pdf.
- Permitir subir un archivo a la vez.
- Guardar los archivos (imagenes, pdf) en un Bucket de S3.
- Registrar nuevos usuarios usando Cognito.
- LogIn de los usuarios usando Cognito.

<br>
<br>

### Ejecutar

##### Desde Shell

```bash
$ npm install
$ npm run start
```

- Abrir browser en: `http://localhost:3000`

##### Desde Docker

- Construir una imagen llamada `code-puk`.

```bash
$ docker build -t code-puk .
```

- Listar imagenes

```bash
$ docker images
```

- **(Opcion 1)** Ejecutar contenedor con modo interactivo

```bash
$ docker run -it -p 4000:3000 code-puk
```

- **(Opcion 2)** Ejecutar contenedor segundo plano

```bash
$ docker run -d -p 4000:3000 code-puk
```

- **(Opcion 3)** Ejecutar `docker-compose.yml`

```bash
$ docker-compose up -d
```

- Busca `IP-ADDRESS` del contenedor

```bash
$ docker-machine ip
```

- Abrir browser en: `http://IP-ADDRESS:4000`

- Explorar directorio `'/app'` del contenedor.

```bash
$ docker exec -it <container-id> /bin/sh
```
