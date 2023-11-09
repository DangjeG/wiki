import React, {useEffect, useState} from "react";
import {api} from "../Configs/app.config";
import {Box, List, ListItemButton, ListItemText, ListSubheader, Tooltip} from "@mui/material";
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";

import {Form, Modal} from "react-bootstrap";
import AccountTreeIcon from '@mui/icons-material/AccountTree';

export default function WorkspaceSelect (props) {

    const [workspaces, setWorkspaces] = useState([]);
    const [newWorkspace, setNewWorkspace] = useState([]);
    const [show, setShow] = useState(false);
    const fetchData = async () => {
        try {
            const response = await api.getWorkspaces();
            setWorkspaces(response);
        } catch (error) {
            console.log(error)
        }
    };

    useEffect(() => {
        props.onSelect("")
        fetchData();
    }, []);

    const handleClick = (id) => {
        props.onSelect(id)
        window.location.hash = "#workspace/docs"
    }


    const handleClose = () => {

        setShow(false)
    };
    const handleShow = () => setShow(true);

    const handleAdd = async () => {
        await api.addWorkspace(newWorkspace)
        handleClose()
        setWorkspaces([])
        fetchData()
    }

    return (
        <>
            <Form.Group className="mb-3"  style={{width: '360px', marginTop: '70px'}}>
                <Form.Control as="textarea" rows={1}
                              placeholder="Поиск"/>
            </Form.Group>
            <List
                sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper'}}
                component="nav"
                aria-labelledby="nested-list-subheader"
                subheader={
                    <ListSubheader component="div" id="nested-list-subheader"  sx={{display: 'flex', justifyContent: 'space-between', marginTop: '10px'}}>
                        Список проектов

                        <Button sx={{border: 'none', outline: 'none' }}
                                variant="outlined" onClick={handleShow}>
                            <Tooltip sx={{width: '10px', height: '10px'}}
                                     title="Добавить проект"
                                     placement="top"
                                     arrow>
                                <AddIcon sx={{color: '#000000'}}/>
                            </Tooltip>
                        </Button>

                    </ListSubheader>
                }
            >
                {Array.from(workspaces).map((workspace) =>
                    <ListItemButton key={workspace.title} onClick={() => {
                        handleClick(workspace.id)
                    }}>
                        <AccountTreeIcon sx={{marginRight: '15px'}}/>
                        <ListItemText primary={workspace.title} />
                    </ListItemButton>
                )}
            </List>

            <Modal show={show} onHide={handleClose}
                   style={{overflow: 'auto', width: '400px', height: '550px', position: 'absolute',
                       left: '50%',
                       top: '55%',
                       transform: 'translate(-50%, -50%)',
                       display: 'flex',
                       justifyContent: 'center',
                       alignItems: 'center',}}>
                <Modal.Header>
                    <Modal.Title>Добавить проект</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Название</Form.Label>
                            <Form.Control value={newWorkspace} onChange={(event) => setNewWorkspace(event.target.value)}/>
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button id="base-button" variant="outlined" onClick={handleClose}>Закрыть</Button>
                    <Box sx={{ marginLeft: '10px' }}></Box>
                    <Button id="accent-button" variant="contained" onClick={handleAdd}>Сохранить</Button>
                </Modal.Footer>
            </Modal>
        </>
    )
}