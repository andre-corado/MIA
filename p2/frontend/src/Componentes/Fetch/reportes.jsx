// CONSTANTE PARA LA DESCARGA DE REPORTES POR MEDIO DEL NOMBRE DE LA IMAGEN (modalInput == nombreImagen)
export const handle_ApiReporte = (e, modalInput) => {
    e.preventDefault(); // Evitar el comportamiento predeterminado, como la recarga de la página en un formulario.

    const nombreArchivo = modalInput + ".svg";

    // Crea un enlace <a> para descargar la imagen.
    fetch(`http://localhost:8000/api-reporte/${nombreArchivo}`)
        .then(response => {
            if (response.ok) {
                // La solicitud fue exitosa, maneja la imagen aquí
                return response.blob();
            } else {
                // Maneja errores aquí
                alert('Error al obtener la imagen:', response.status, response.statusText);
            }
        })
        .then(blob => {
            // Convierte el blob en una URL de objeto y muestra la imagen
            const imageUrl = URL.createObjectURL(blob);

            // Crea un enlace para descargar la imagen
            const downloadLink = document.createElement('a');
            downloadLink.href = imageUrl;
            downloadLink.download = nombreArchivo; // Utiliza el nombre del archivo
            downloadLink.style.display = 'none';

            document.body.appendChild(downloadLink); // Agrega el enlace al cuerpo del documento
            downloadLink.click(); // Esto desencadenará la descarga automáticamente.
            document.body.removeChild(downloadLink); // Elimina el enlace después de la descarga.
        })
        .catch(error => { alert('Error en la solicitud:', error); });
};