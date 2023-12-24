import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";
import {Box, List, ListItemButton, ListItemText, ListSubheader, Tooltip} from "@mui/material";
import {Form} from "react-bootstrap";
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import ButtonAddWorkspace from "../Components/ModalButton/ButtonAddWorkspace";
import {useNavigate, useParams} from "react-router-dom";

export default function WorkspaceSelect () {

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
            <List
                sx={{margin:"100px 50px", width: '100%', maxWidth: 360, bgcolor: 'background.paper'}}
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