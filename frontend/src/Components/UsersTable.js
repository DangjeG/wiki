import React, { useEffect, useState } from 'react';
import { Button, FormControlLabel, FormLabel, Modal, Radio, RadioGroup, Table } from '@mui/material';
import { api } from '../app.config';
import { Box } from '@mui/system';

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
            <Box sx={{width: '100%', margin: '10px', padding: '50px 50px', background: '#d4b0ce',  borderRadius: '8px'}} >
                <Table >
                    <thead>
                    <tr key="header">
                        <th style={{ background: '#d4b0ce', border: 'none' }}>Email</th>
                        <th style={{ background: '#d4b0ce', border: 'none' }}>Username</th>
                        <th style={{ background: '#d4b0ce', border: 'none' }}>Full name</th>
                        <th style={{ background: '#d4b0ce', border: 'none' }}>Responsibility</th>
                    </tr>
                    </thead>
                    <tbody>
                    {users.map((user) => (
                        <tr key={user.username}>
                            <td style={{ background: '#d4b0ce', border: 'none' }}>{user.email}</td>
                            <td style={{ background: '#d4b0ce', border: 'none' }}>{user.username}</td>
                            <td style={{ background: '#d4b0ce', border: 'none' }}>{user.first_name + ' ' + user.last_name + ' ' + user.second_name}</td>
                            <td style={{ background: '#d4b0ce', border: 'none' }}>
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
                <Modal open={show} onClose={handleClose}>
                    <Box sx={{ padding: '20px' }}>
                        <h2>Approve user</h2>
                        <FormLabel>Description</FormLabel>
                        <textarea
                            value={description}
                            onChange={(event) => setDescription(event.target.value)}
                            rows={3}
                            style={{ width: '100%' }}
                        />
                        <Box sx={{ display: 'flex', alignItems: 'center', marginTop: '10px' }}>
                            <FormLabel>Responsibility</FormLabel>
                            <RadioGroup
                                row
                                value={responsibility}
                                onChange={(event) => setResponsibility(event.target.value)}
                            >
                                <FormControlLabel control={<Radio />} label="VIEWER" value="VIEWER" />
                                <FormControlLabel control={<Radio />} label="EDITOR" value="EDITOR" />
                                <FormControlLabel control={<Radio />} label="ADMIN" value="ADMIN" />
                            </RadioGroup>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: '20px' }}>
                            <Button variant="contained" onClick={handleClose} sx={{ marginRight: '10px' }}>
                                Close
                            </Button>
                            <Button variant="contained" onClick={handleClose}>
                                Save Changes
                            </Button>
                        </Box>
                    </Box>
                </Modal>
            </Box>
        </div>
    );
}
