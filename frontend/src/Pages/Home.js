import React, {useEffect, useState} from "react";
import {api} from "../app.config";
import {List, ListItemButton, ListItemText, ListSubheader} from "@mui/material";


function SendIcon() {
    return null;
}

export default function Home(){

    const [workspaces, setWorkspaces] = useState([]);


    useEffect(() => {
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
                <ListItemButton key={workspace.title}>
                    <ListItemText primary={workspace.title}/>
                </ListItemButton>
            )}
            </List>
        </>
    )
}