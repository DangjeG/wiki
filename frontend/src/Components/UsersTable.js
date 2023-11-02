import React, { useEffect, useState } from 'react';
import {Button, Form, Modal, Table} from "react-bootstrap";
import { api } from '../app.config';
import { Box } from '@mui/system';
import {FormControlLabel, FormLabel, Radio, RadioGroup} from "@mui/material";

export default function UsersTable() {
    const [users, setUsers] = useState([]);
    const [show, setShow] = useState(false);
    const [description, setDescription] = useState('');
    const [responsibility, setResponsibility] = useState('');
    const [username, setUsername] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getUsers();
                setUsers(response);
            } catch (error) {
                console.log(error);
            }
        };
        fetchData();
    }, []);

    const handleClose = () => {
        approve();
        setShow(false);
    };

    const handleShow = () => {
        setShow(true);
    };

    function approve() {
        api.approveUser(username, responsibility, description);
        fetchData();
        setResponsibility('');
        setDescription('');
        setUsername('');
    }

    const fetchData = async () => {
        try {
            const response = await api.getUsers();
            setUsers(response);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div style={{"padding": "10px 70px"}}>
            <Box sx={{width: '100%', margin: '10px', padding: '50px 50px', background: '#cdf',  borderRadius: '8px'}} >
                <Table >
                    <thead>
                    <tr key="header">
                        <th style={{ background: '#cdf', border: 'none' }}>Email</th>
                        <th style={{ background: '#cdf', border: 'none' }}>Username</th>
                        <th style={{ background: '#cdf', border: 'none' }}>Full name</th>
                        <th style={{ background: '#cdf', border: 'none' }}>Responsibility</th>
                    </tr>
                    </thead>
                    <tbody>
                    {users.map((user) => (
                        <tr key={user.username}>
                            <td style={{ background: '#cdf', border: 'none' }}>{user.email}</td>
                            <td style={{ background: '#cdf', border: 'none' }}>{user.username}</td>
                            <td style={{ background: '#cdf', border: 'none' }}>{user.first_name + ' ' + user.last_name + ' ' + user.second_name}</td>
                            <td style={{ background: '#cdf', border: 'none' }}>
                                {user.wiki_api_client === null ? (
                                    <Button onClick={() => {
                                        setUsername(user.username);
                                        handleShow();
                                    }}>
                                        Approve
                                    </Button>
                                ) : (
                                    user.wiki_api_client.responsibility
                                )}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </Table>
                <Modal show={show} onHide={handleClose}>
                    <Modal.Header>
                        <Modal.Title>Add organization</Modal.Title>
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
                        <Button variant="primary" onClick={approve}>
                            Save Changes
                        </Button>
                    </Modal.Footer>
                </Modal>
                <Button style={{ background: '#cdf', border: 'none' }} variant="light" onClick={handleShow}>+</Button>
            </Box>
        </div>
    );
}
