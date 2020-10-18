const { Router } = require('express');
const AmazonCognitoIdentity = require('amazon-cognito-identity-js');
const AWS = require('aws-sdk');
const fs = require('fs-extra');
const custom_env = require('custom-env')
global.fetch = require('node-fetch');



// Inicializar
const router = Router();

custom_env.env();

const s3 = new AWS.S3({
    accessKeyId: process.env.AWS_ID,
    secretAccessKey: process.env.AWS_SECRET
});

const poolData = {
    UserPoolId: process.env.USERPOOLID,
    ClientId: process.env.CLIENTID
}

const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);



// Routes
router.get('/', (req, res) => {
    // Redirecciona a un '.html' en 'src/views'
    res.render('index');
})

router.get('/login', (req, res) => {
    // Redirecciona a un '.html' en 'src/views'
    res.render('login');
})

router.post('/login', (req, res) => {

    var loginDetails = {
        // Obtener datos del form
        Username : req.body.txtEmail,
        Password : req.body.txtPassword
    };

    const authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(loginDetails);

    const userDetails = {
        Username : req.body.txtEmail,
        Pool : userPool
    };

    const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userDetails);
    
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: data => {
            console.log(data);
            
            // Crear una sesion
            req.session.my_email = req.body.txtEmail;

            res.redirect('/home');
        },
        onFailure: err => {
            console.log(err);
            //req.session['login-error'].push(err.message);
            res.redirect('/login');
        }
    });
})

router.get('/register', (req, res) => {
    // Redirecciona a un '.html' en 'src/views'
    res.render('register');
})

router.post('/register', (req, res) => {

    // Obtener datos del form
    const email  = req.body.txtEmail;
    const password  = req.body.txtPassword;


    const emailData = {
        Name: 'email',
        Value: email
    };

    // Recopilar los campos para ser validado (email, number phone, ...) por Cognito
    const attributeList = [];
    const emailAttribute = new AmazonCognitoIdentity.CognitoUserAttribute(emailData);
    attributeList.push(emailAttribute);

    // Registra al usuario en Cognito
    userPool.signUp(email, password, attributeList, null, (err, data) => {
        if (err) {
            return console.error(err);
        }
        // Respuesta satisfactoria de Cognito
        //res.send(data.user);
    });

    // Redirecciona a un '.html' en 'src/views'
    res.render('login');
})

router.get('/home', (req, res) => {
    // Redirecciona a un '.html' en 'src/views'
    res.render('home');
})

router.post('/home', async (req, res) => {
    // Informacion de la Data Enviada
    //console.log(req.file);

    // Obtener file de '/public/uploads'
    const fileContent = fs.readFileSync(req.file.path);

    // Parametros de configuracion para S3
    const params = {
        Bucket: process.env.AWS_BUCKET_NAME,
        Key: req.file.filename,
        Body: fileContent
    };

    // Subir archivos al Bucket
    const result = await s3.upload(params, function(err, data) {
        if (err) {
            throw err
        }
        console.log(`File uploaded successfully. ${data.Location}`)
    });

    // Eliminar file de '/public/uploads' despues ser subida
    await fs.unlink(req.file.path);

    // Respuesta de S3
    console.log(result)

    // Redirecciona a un '.html' en 'src/views'
    res.render('home');
})

router.get('/logout', (req, res) => {
    // Eliminar la sesion
    delete req.session.my_email;

    // Redirecciona a un '.html' en 'src/views'
    res.redirect('/');
})



// Exporta los modulos para ser requeridos desde otro archivos
module.exports = router;