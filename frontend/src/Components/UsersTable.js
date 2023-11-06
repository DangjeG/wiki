import React, { useEffect, useState } from 'react';
import { Box, Button, FormControlLabel, FormLabel, Radio, RadioGroup, Table, Tooltip } from '@mui/material';
import { api } from '../app.config';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import AddIcon from '@mui/icons-material/Add';
import {Form, Modal} from "react-bootstrap";
import "../Styles/BaseColors.css"

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
        <div style={{display: 'flex'}}>
            <Button style={{ background: '#cdf', border: 'none', width: '1%', height: '7%', position: 'absolute', left: '5%', top: '30%'}}
                    variant="outlined"
                    onClick={handleShow}>
                <Tooltip sx={{width:'8%', height:'-5%', marginBottom: '2%', marginRight:'1%'}}
                         title="Добавить пользователя"
                         placement="top"
                         arrow>
                    <AddIcon sx={{color:'#000000'}}/>
                </Tooltip>

            </Button>
            <Box sx={{ container:'true', margin: '10px', padding: '50px 50px', background: '#cdf',  borderRadius: '10px', width:'100%' }}>
                <Table sx={{borderCollapse: 'collapse', width: '100%'}}>
                    <thead>
                    <tr key="header">
                        <th style={{ background: '#cdf', border: 'none' }}>
                            <Tooltip sx={{width:'8%', height:'-5%', marginBottom: '2%', marginRight:'1%'}}
                                     title="email пользователя - его контактная почта, куда можно отправить код"
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Email
                        </th>
                        <th style={{ background: '#cdf', border: 'none' }}>
                            <Tooltip sx={{width:'8%', height:'-5%', marginBottom: '2%', marginRight:'1%'}}
                                     title="Логин используется пользователем для входа в систему"
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Логин
                        </th>
                        <th style={{ background: '#cdf', border: 'none' }}>
                            <Tooltip sx={{width:'8%', height:'-5%', marginBottom: '2%', marginRight:'1%'}}
                                     title="Фамилия, имя и отчество пользователя"
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            ФИО
                        </th>
                        <th style={{ background: '#cdf', border: 'none' }}>
                            <Tooltip sx={{width:'8%', height:'-5%', marginBottom: '2%', marginRight:'1%'}}
                                     title={<span><strong>Зритель</strong> - будет описание.<br/>
                                            <strong>Редактор</strong> - будет описание.<br/>
                                            <strong>Админ</strong> - будет описание.
                                            </span>}
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Роль
                        </th>
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
                        <Modal.Title>Добавить пользователя</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group className="mb-3">
                                <Form.Label>Описание</Form.Label>
                                <Form.Control
                                    value={description}
                                    onChange={(event) => setDescription(event.target.value)}
                                    as="textarea"
                                    rows={3}
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <FormLabel component="legend">Роль</FormLabel>
                                <RadioGroup aria-label="responsibility" value={responsibility} onChange={(event) => setResponsibility(event.target.value)}>
                                    <FormControlLabel value="VIEWER" control={<Radio />} label="ЗРИТЕЛЬ" />
                                    <FormControlLabel value="EDITOR" control={<Radio />} label="РЕДАКТОР" />
                                    <FormControlLabel value="ADMIN" control={<Radio />} label="АДМИН" />
                                </RadioGroup>
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button id="base-button" variant="outlined" onClick={handleClose}>Закрыть</Button>
                        <Box sx={{ marginLeft: '10px' }}></Box>
                        <Button id="accent-button" variant="contained" onClick={approve}>Сохранить</Button>
                    </Modal.Footer>
                </Modal>
            </Box>

        </div>
    );
}