import React, {useEffect, useState} from 'react';
import List from '@mui/material/List';
import {Box, Grid, Tooltip, Typography} from "@mui/material";
import DirectoryListItem from "./DirectoryListItem";
import {api} from "../Configs/app.config";
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import {Form, Modal} from "react-bootstrap";
export default function Sidebar(props){

    const [show, setShow] = useState(false);
    const [sidebarData, setSidebarData] = useState([]);
    const [newDocument, setNewDocument] = useState()
    const [disableAddButton, setDisableAddButton] = useState(false)
    const [workspace, setWorkspace] = useState(null)
    const fetchData = async () => {
        try {
            const response = await api.getDocumentsTree(props.workspaceID)
            setSidebarData(response)
            props.onSelect(response[0].id)
        }
        catch (e){
            console.log(e)
        }
    };

    const fetchWorkspace = async () =>{
        try{
            const response = await api.getWorkspaceInfo(props.workspaceID)
            setWorkspace(response)
        }
        catch (e){
            console.log(e)
        }
    }

    useEffect(() => {
        fetchWorkspace()
        fetchData()
    }, []);


    const handleClose = () => setShow(false)

    const handleShow = () => setShow(true);

    const handleAdd = async () => {
        setDisableAddButton(true)
        await api.addDocument(newDocument, props.workspaceID)
        handleClose()
        setSidebarData([])
        fetchData()
        setDisableAddButton(false)
    }

    const handleClick = (id) => {
        props.onSelect(id)
    }

    function getChildren(children) {
        if (children === null) return null
        return children.map((item) => (
            <DirectoryListItem onClick={handleClick} id={item.id} title={item.title} children={getChildren(item.children)} />
        ));
    }

    return (
        <>
            <Grid
                container
                justifyContent="center"
                height="100%"
                sx={{background: '#ffffff', color: '#000000', marginTop: '20px', height: '100vh'}}
            >
                <Grid item>
                    <Typography fontWeight="bold">
                        {workspace ? workspace.title: null}
                    </Typography>
                    <List>
                        {sidebarData.map((item) =>
                        {
                            return <DirectoryListItem onClick={handleClick} id={item.id} title={item.title} children={getChildren(item.children)} />
                        })}
                    </List>

                    <Button id='accent-button'
                            variant="outlined"
                            sx={{ marginBottom: '0px' }}
                            onClick={handleShow}>
                        <Tooltip sx={{width: '10px', height: '10px'}}
                                 title="Добавить документ"
                                 placement="top"
                                 arrow>
                            Добавить
                            <AddIcon sx={{color: '#000000'}}/>
                        </Tooltip>
                    </Button>

                </Grid>
            </Grid>

            <Modal show={show} onHide={handleClose}
                   style={{overflow: 'auto', width: '400px', height: '550px', position: 'absolute',
                       left: '50%',
                       top: '55%',
                       transform: 'translate(-50%, -50%)',
                       display: 'flex',
                       justifyContent: 'center',
                       alignItems: 'center',}}>
                <Modal.Header>
                    <Modal.Title>Добавить документ</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Название</Form.Label>
                            <Form.Control value={newDocument} onChange={(event) => setNewDocument(event.target.value)} />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button id="base-button" variant="outlined" onClick={handleClose}>Закрыть</Button>
                    <Box sx={{ marginLeft: '10px' }}></Box>
                    <Button disabled={disableAddButton} id="accent-button" variant="contained" onClick={handleAdd}>Сохранить</Button>
                </Modal.Footer>
            </Modal>
        </>
    );
};

