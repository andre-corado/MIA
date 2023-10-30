import { Button, Container, Form, Row, Modal } from "react-bootstrap"
import NavScrollExample from "../Navbar/Navbar_"
import { useState } from 'react';
import './css/Style.css'
import { handle_ApiExecute } from "../Fetch/execute";
import { handle_ApiLogin } from "../Fetch/Login";

const Dashboard = () => {
    const [textoEntrada, setTextoEntrada] = useState('');
    const [textoSalida, setTextoSalida] = useState('');


    // Abrir un archivo
    const handleFileChange = (e) => {
        const file = e.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = (event) => {
                const text = event.target.result;
                setTextoEntrada(text);
            };

            reader.readAsText(file);
        } else {
            setTextoEntrada('');
        }
    };

    // Limpiar cajas de texto
    const handleCleanBtn = (e) => {
        e.preventDefault();
        setTextoEntrada('');
        setTextoSalida('');
    }


    // BARRA BUSQUEDA DE REPORTES
    const [show, setShow] = useState(false);
    const handleShow = () => setShow(true);

    // MODAL LOGIN
    const handleClose = () => setShow(false);


    // ------------------------------------------- LOGIN -------------------------------------------
    const [usuario, setUsuario] = useState('');
    const [idDisco, setIdDisco] = useState('');
    const [contrasena, setContrasena] = useState('');

    const handleUsuarioChange = (event) => {
        setUsuario(event.target.value);
    };

    const handleIdDiscoChange = (event) => {
        setIdDisco(event.target.value);
    };

    const handleContrasenaChange = (event) => {
        setContrasena(event.target.value);
    };

    // ------------------------------------------- LOGOUT  -------------------------------------------
    const [formDisabled, setFormDisabled] = useState(true);

    return (
        <>
            <Container fluid>
                <Row>
                    <NavScrollExample
                        handleFileChange={handleFileChange}
                        handleShow={handleShow}
                        formDisabled={formDisabled}
                        setFormDisabled={setFormDisabled}
                    />
                </Row>
        
                <Row id="container-file" className="my-4">
                    <div className="d-grid gap-2 col-md-6 mx-auto">
                        <Button variant="primary" size="lg" onClick={(e) => handle_ApiExecute(e, textoEntrada, setTextoSalida)}>
                            Ejecutar Comandos
                        </Button>
                        <Button variant="secondary" size="lg" onClick={handleCleanBtn}>
                            Limpiar Cajas de texto
                        </Button>
                    </div>
                </Row>
            
                <Row id="container-textboxE" className="d-flex justify-content-center align-items-center">
                    <Form.Group className="mb-5" id="container-textArea1">
                        <Form.Label className="lbl-titulo">Entrada</Form.Label>
                        <Form.Control as="textarea" rows={18} id="textArea-entrada" value={textoEntrada} onChange={(e) => setTextoEntrada(e.target.value)}/>
                    </Form.Group>
                </Row>


            
                <Row id="container-textboxS" className="d-flex justify-content-center align-items-center">
                    <Form.Group className="mb-5" id="container-textArea1">
                        <Form.Label className="lbl-titulo">Salida</Form.Label>
                        <Form.Control as="textarea" rows={18} id="textArea-salida" value={textoSalida} onChange={(e) => setTextoSalida(e.target.value)}/>
                    </Form.Group>
                </Row>

            </Container>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Login</Modal.Title>
                </Modal.Header>
                <Modal.Body>

                <Form>
                    <Form.Group className="mb-3" controlId="formGroupUsuario">
                        <Form.Label>Usuario</Form.Label>
                        <Form.Control type="text" value={usuario} onChange={handleUsuarioChange} />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formGroupIdDisco">
                        <Form.Label>ID Disco</Form.Label>
                        <Form.Control type="text" value={idDisco} onChange={handleIdDiscoChange} />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formGroupContrasena">
                        <Form.Label>Contraseña</Form.Label>
                        <Form.Control type="password" value={contrasena} onChange={handleContrasenaChange} />
                    </Form.Group>
                </Form>
                
                </Modal.Body>
                <Modal.Footer>
                <Button variant="primary" onClick={ (e) => handle_ApiLogin(e, usuario, contrasena, idDisco, setUsuario, setContrasena, setIdDisco, handleClose, setFormDisabled) }>Ingresar</Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}

export default Dashboard