import {Nav, Navbar, Dropdown, Button} from "react-bootstrap";
import {useEffect, useState} from "react";
import {api} from "../app.config";
import {User} from "../Models/User";


export default function AppNavbar(props){

    const [user, setUser] = useState(new User())

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getMe();
                setUser(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
    }, []);

    function getRightPanel(){

        if (!props.isLogin){
            return(
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
                            {user.username}
                        </Dropdown.Toggle>
                        <Dropdown.Menu variant="dark" >
                            <Dropdown.Item href="/profile">Profile</Dropdown.Item>
                            {addAdmin()}
                            <Dropdown.Divider/>
                            <Dropdown.Item href="/logout">Logout</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </Nav>
            )
        }
    }

    function addAdmin(){
        if (user.responsibility === "ADMIN") return(<Dropdown.Item href="/admin">Admin Tools</Dropdown.Item>)
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
