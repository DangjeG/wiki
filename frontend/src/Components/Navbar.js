import {Nav, Navbar} from "react-bootstrap";
import React from "react";



export default function AppNavbar() {
    return (
        <>
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
                <Navbar.Brand href="/">Home</Navbar.Brand>

                <Navbar.Collapse id="responsetive-navbar-nav">
                    <Nav className="me-auto my-2 my-lg-0"
                         style={{ maxHeight: '100px' }}
                         navbarScroll
                    >
                    </Nav>
                    <Nav>
                        <Nav.Link href="/login" className="mr-2">Login</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
                <Navbar.Toggle aria-controls="responsetive-navbar-nav"/>
            </Navbar>
        </>
    )
}
