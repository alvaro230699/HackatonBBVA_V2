$(document).ready(function() { 
    // Envita error al no encontrar el id 'inputGroupFile01' en otras rutas diferentes a '/home'
     try {
        if (document.getElementById("inputGroupFile01")) {
            const input = document.getElementById("inputGroupFile01");
            input.onchange = function() {
                const file = this.files;
                if (file.length > 0) {
                    // Habilita el button si selecciono un file
                    document.getElementById("btnEnviar").disabled = false;
                } else {
                    document.getElementById("btnEnviar").disabled = true;
                }
            }
        }
    } catch (e) {

    }
    /*
    $(".txtPassword").on("click", function() {
        const pass = document.getElementById("txtPassword")
        function checkPassword(pass)
        {
            // at least one number, one lowercase and one uppercase letter
            // at least six characters
            var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/;
            return re.test(pass);
        }
    });*/
});