import {Nav, Navbar} from "react-bootstrap";
import React, {useState} from "react";


export default function AppNavbar(props){

    function getRightPanel(){
        if (!props.isLogin){
            return(
                <Nav>
                    <Nav.Link href="/login" className="mr-2">Login</Nav.Link>
                    <Nav.Link href="/signup" className="mr-2">Sign Up</Nav.Link>
                </Nav>
            )
        }
        else {
            return (
                <Nav>
                    <Nav.Link href="/" className="mr-2" onClick={()=>
                    {
                        localStorage.setItem("token", null)
                    }}>Logout</Nav.Link>
                </Nav>
            )
        }
    }


    return (
        <>
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
                <Navbar.Brand href="/">Home</Navbar.Brand>

                <Navbar.Collapse id="responsetive-navbar-nav">
                    <Nav className="me-auto my-2 my-lg-0"
                         style={{maxHeight: '100px'}}
                         navbarScroll
                    >
                    </Nav>
                    {getRightPanel()}
                </Navbar.Collapse>
                <Navbar.Toggle aria-controls="responsetive-navbar-nav"/>
            </Navbar>
        </>
    )
}
