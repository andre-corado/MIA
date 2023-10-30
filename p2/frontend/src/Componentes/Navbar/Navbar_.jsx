import { Navbar, Container, Nav, Form, Button } from "react-bootstrap";
import { handle_ApiLogout } from "../Fetch/logout";
import { handle_ApiReporte } from "../Fetch/reportes";
import { useState } from 'react';

const NavScrollExample = ({ handleFileChange, handleShow, formDisabled, setFormDisabled }) => {

    const handleOpenFile = () => {
        document.getElementById("file-input").click();
    };

    // boton de reportes
    const [searchText, setSearchText] = useState(''); // Estado para el valor del campo de búsqueda

    return (
        <Navbar expand="lg" className="bg-body-tertiary">

            <Container fluid>

                <Navbar.Brand >202100154</Navbar.Brand>

                <Navbar.Toggle aria-controls="navbarScroll" />
                <Navbar.Collapse id="navbarScroll">
                <Nav
                    className="me-auto my-2 my-lg-0"
                    style={{ maxHeight: '100px' }}
                    navbarScroll
                >
                    <Form>
                        <Nav.Link onClick={handleOpenFile}>File</Nav.Link>
                        <Form.Control type="file" id="file-input" onChange={handleFileChange} style={{ display: "none" }} />
                    </Form>
                    <Nav.Link onClick={handleShow}>Login</Nav.Link>
                    <Nav.Link onClick={ (e) => handle_ApiLogout(e, setFormDisabled) }>Logout</Nav.Link>
                </Nav>

                <Form className="d-flex">
                    <Form.Control
                        type="search"
                        placeholder="Search Report"
                        className="me-2"
                        aria-label="Search"
                        value={searchText}
                        onChange={(e) => setSearchText(e.target.value)}
                        disabled={formDisabled}
                    />
                    <Button variant="outline-success" disabled={formDisabled} onClick={(e) => handle_ApiReporte(e, searchText)}>Search</Button>
                </Form>

                </Navbar.Collapse>

            </Container>

            

        </Navbar>
    );
}

export default NavScrollExample;