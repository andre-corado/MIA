// CONSTANTE PARA EJECUTAR EL TEXTO DE ENTRADA
export const handle_ApiExecute = async (e, fileContent, setConsoleContent) => {
    let salida = "";

    // Reemplaza caracteres de retorno de carro ('\r') con nada (eliminándolos).
    let data = fileContent.replace(/\r/g, '');

    // Divide el texto en un array de líneas.
    let arregloContent = data.split('\n');

    // Filtra las líneas que no están vacías y no comienzan con '#'.
    arregloContent = arregloContent.filter(elemento => elemento.trim() !== '' && !elemento.trim().startsWith('#'));

    try {
        for (let i = 0; i < arregloContent.length; i++) {
            e.preventDefault();
            const data = { entrada: arregloContent[i] };
            
            const response = await fetch(`http://localhost:8000/api-execute`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud para ${arregloContent[i]}`);
            }

            const responseData = await response.json();

            if (responseData.salida.toLowerCase() === 'pause') {
                setConsoleContent(salida);
                var alerta = 'Comando a ejecutar:\n' + arregloContent[i+1]
                alert(alerta);
                continue;
            }

            salida += 'COMANDO -->>> ' + arregloContent[i] + '\n';
            salida += responseData.salida;
            setConsoleContent(salida);
        }
    } catch (error) {
        alert(error.message);
    }

    setConsoleContent(salida);
};