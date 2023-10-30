// CONSTANTE PARA EL MANEJO DE LOGOUT
export const handle_ApiLogout = (e, setFormDisabled) => {
    e.preventDefault(); // Prevenir el comportamiento predeterminado, como la recarga de la página en un formulario.

    // Envía los datos a la API
    const data = { entrada: 'Logout' }
    fetch(`http://localhost:8000/api-logout`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then((res) => res.json())
    .then((data) => { 
        alert(data["salida"])
    })
    .catch((error) => { alert(error); });

    setFormDisabled(true);
};