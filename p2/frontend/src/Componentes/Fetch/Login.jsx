// CONSTANTE PARA EL MANEJO DE REGISTRO DE USUARIOS
export const handle_ApiLogin = (e, usuario, contrasena, idDisco, setUsuario, setContrasena, setIdDisco, handleClose, setFormDisabled) => {
    e.preventDefault(); // Prevenir el comportamiento predeterminado, como la recarga de la página en un formulario.

    // Toma los valores y da formato para ser enviados a la API
    var comando = 'Login -pass=' + contrasena + ' -user=' + usuario + ' -id=' + idDisco;

    // Envía los datos a la API
    const data = { entrada: comando }
    fetch(`http://localhost:8000/api-login`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then((res) => res.json())
    .then((data) => {
        if (data["salida"].includes('<<<Ocurrio un error>>>')){
            alert(data["salida"]);

        }else if (data["salida"].includes('<<<Ejecutado>>>')){
            alert(data["salida"]);
            setFormDisabled(false);
        }
    })
    .catch((error) => { alert(error); });

    // REINICIA TODOS LOS CAMPOS CON UNA CADENA VACIA
    setUsuario('');
    setIdDisco('');
    setContrasena('');

    // CIERRA EL MODAL
    handleClose()
};