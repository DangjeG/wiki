import React, {useEffect, useState} from "react";
import {api} from "../app.config";
import {List, ListItemButton, ListItemText, ListSubheader} from "@mui/material";


export default function WorkspaceSelect (props) {

    const [workspaces, setWorkspaces] = useState([]);


    useEffect(() => {
        props.onSelect("")
        const fetchData = async () => {
            try {
                const response = await api.getWorkspaces();
                setWorkspaces(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
    }, []);

    const handleClick = (id) => {
        props.onSelect(id)
        window.location.hash = "#workspace/docs"
    }

    return (
        <>
            <List
                sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}
                component="nav"
                aria-labelledby="nested-list-subheader"
                subheader={
                    <ListSubheader component="div" id="nested-list-subheader">
                        List of workspaces
                    </ListSubheader>
                }
            >
                {Array.from(workspaces).map((workspace) =>
                    <ListItemButton key={workspace.title} onClick={() => {
                        handleClick(workspace.id)
                    }}>
                        <ListItemText primary={workspace.title} />
                    </ListItemButton>
                )}
            </List>
        </>
    )
}