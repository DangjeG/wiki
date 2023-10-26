import {Button, Dropdown, Nav, Navbar} from "react-bootstrap";



export default function AppNavbar(props){

    function getRightPanel(){


        if (props.user === null) {
            return (
                <Nav>
                    <Button variant="dark" href="/login" className="mr-2">Login</Button>
                    <Button variant="dark" href="/signup" className="mr-2">Sign Up</Button>
                </Nav>
            )
        }
        else {
            return (
                <Nav>
                    <Dropdown>
                        <Dropdown.Toggle variant="dark" id="dropdown-basic">
                            {props.user.username}
                        </Dropdown.Toggle>
                        <Dropdown.Menu variant="dark">
                            <Dropdown.Item href="/profile">Profile</Dropdown.Item>
                            {props.user.wiki_api_client.responsibility === "ADMIN" ?
                                <Dropdown.Item href="/admin">Admin Tools</Dropdown.Item> : <></>}
                            <Dropdown.Divider/>
                            <Dropdown.Item href="/logout">Logout</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </Nav>)
        }
    }

    return (
        <>
            <Navbar collapseOnSelect expand="lg" style={{"paddingRight": "50px", "paddingLeft": "50px"}} bg="dark" variant="dark">
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
