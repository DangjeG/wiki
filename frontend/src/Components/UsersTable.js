import {Button, Form, Modal, Table} from "react-bootstrap";
import {api} from "../app.config";
import React, {useEffect, useState} from "react";


export default function UsersTable() {

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getUsers();
                setUsers(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
    }, []);


    const [users, setUsers] = useState([]);
    const [show, setShow] = useState(false);

    const [description, setDescription] = useState("");
    const [responsibility, setResponsibility] = useState("");
    const [username, setUsername] = useState("");



    function approve() {


    }

    const handleClose = () => {
        Approve()
        setShow(false)
    };
    const handleShow = () => {
        setShow(true);
    }


    function Approve(){
        api.approveUser(username, responsibility, description)
        const fetchData = async () => {
            try {
                const response = await api.getUsers();
                setUsers(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();

        setResponsibility("")
        setDescription("")
        setUsername("")

    }



    return (
        <div style={{"padding": "50px 150px"}}>
            <Table>
                <thead>
                <tr key={"header"}>
                    <th>Email</th>
                    <th>Username</th>
                    <th>Full name</th>
                    <th>Responsibility</th>
                </tr>
                </thead>
                <tbody>
                {Array.from(users).map((user) => (
                    <tr key={user.username}>
                        <td>{user.email}</td>
                        <td>{user.username}</td>
                        <td>{user.first_name + " " + user.last_name + " " + user.second_name}</td>
                        <td>{user.wiki_api_client === null ?
                            <Button onClick={() =>{
                                setUsername(user.username)
                                handleShow()
                            }}>
                                Approve
                            </Button>
                            : user.wiki_api_client.responsibility}
                        </td>
                    </tr>
                ))}
                </tbody>
            </Table>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header>
                    <Modal.Title>Approve user</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Description</Form.Label>
                            <Form.Control value={description} onChange={(event) => (setDescription(event.target.value))}
                                          as="textarea" rows={3}/>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Check inline type="radio" label={`VIEWER`} name={"group"}
                                        onClick={() => setResponsibility("VIEWER")}/>
                            <Form.Check inline type="radio" label={`EDITOR`} name={"group"}
                                        onClick={() => setResponsibility("EDITOR")}/>
                            <Form.Check inline type="radio" label={`ADMIN`} name={"group"}
                                        onClick={() => setResponsibility("ADMIN")}/>
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    <Button variant="primary" onClick={handleClose}>
                        Save Changes
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    )
}