const express = require('express');
const morgan = require('morgan')
const path = require('path');
const multer = require('multer');
const bodyParser = require('body-parser');
const session = require('express-session');
const flash = require('connect-flash');
//const { v4: uuidv4 } = require('uuid');



// Inicializar
const app = express();



// Configuracion
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));    // indica que la carpeta 'view' esta en '/src/views' y no en '/views' (default)
app.set('view engine', 'ejs');                      // indica el motor de plantilla 'ejs'



// Middleware
app.use(morgan('dev'))

app.use(express.json());

app.use(express.urlencoded({extended: false}));

app.use(session({
    secret: 'mysecretkey',
    resave: false,
    saveUninitialized: false
}));

app.use(flash());

const storage = multer.diskStorage({
    destination: path.join(__dirname, 'public/uploads'),    // Estable el directorio de destino de la imagen subida
    /*filename: (req, file, cb) => {                          // Establece el nombre original de la imagenes subida
        cb(null, file.originalname);
    }*/
    filename: (req, file, cb) => {                          // Estable como nombre un id unico para cada imagen subida
        fl = file.originalname.substring(file.originalname, file.originalname.lastIndexOf('.'))
        cb(null, fl + ";" + req.session.my_email + ";" + Date.now() + path.extname(file.originalname));
    }
});

app.use(multer({
    storage: storage,
    dest: path.join(__dirname, 'public/uploads'),    // Crea el directorio de destino sino existe
    fileFilter: function (req, file, cb) {
        const filetypes = /jpeg|jpg|png|pdf|zip/;           // Extensiones permitidas
        const mimetype = filetypes.test(file.mimetype); // Obtiene la extension de la imagen
        const extname = filetypes.test(path.extname(file.originalname).toLowerCase());  // Define un nombre unico para la imagen subida
        if (mimetype && extname) {
            return cb(null, true);
        }
        cb("Error: No se puede subir ningo archivo con extension diferente a: " + filetypes);
    }
}).single('flImage'));                               // 'single' indica que subira una sola image y 'flImage' en nombre del componente en el form



// Routes
app.use(require(path.join(__dirname, 'routes/index.routes.js')));



// Archivos estaticos
app.use(express.static(path.join(__dirname, 'public')));



// Iniciar Servidor
app.listen(app.get('port'), () => {
    console.log(`Iniciando servidor en http://localhost:${app.get('port')}`);
})