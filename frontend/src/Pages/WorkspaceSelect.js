import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";
import {Box, List, ListItemButton, ListItemText, ListSubheader, Tooltip} from "@mui/material";
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import {Form, Modal} from "react-bootstrap";
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import ButtonAddWorkspace from "../Components/ModalButton/ButtonAddWorkspace";
import {useNavigate, useParams} from "react-router-dom";

export default function WorkspaceSelect (props) {

    const [workspaces, setWorkspaces] = useState([]);
    let navigate = useNavigate()

    const fetchWorkspaces = async () => {
        try {
            const response = await api.getWorkspaces();
            setWorkspaces(response);
        } catch (error) {
            console.log(error)
        }
    };

    useEffect(() => {
        props.onSelect("")
        fetchWorkspaces();
    }, []);

    const handleClick = (id) => {
        navigate(`/workspace/${id}`)
    }

    const handleSubmit = async (newWorkspace) => {
        await api.addWorkspace(newWorkspace)
        setWorkspaces([])
        fetchWorkspaces()
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
                        <ButtonAddWorkspace onSubmit={handleSubmit}/>
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
        </>
    )
}