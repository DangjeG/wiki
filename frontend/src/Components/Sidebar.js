import React, {useEffect, useState} from 'react';
import List from '@mui/material/List';
import {Box, Grid, Tooltip, Typography} from "@mui/material";
import DirectoryListItem from "./DirectoryListItem";
import {api} from "../Config/app.config";
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import {Form, Modal} from "react-bootstrap";
import ButtonAddDocument from "./ModalButton/ButtonAddDocument";
export default function Sidebar(props){


    const [sidebarData, setSidebarData] = useState([]);

    const [workspace, setWorkspace] = useState(null)
    const fetchDocs = async () => {
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
        fetchDocs()
    }, []);



    const handleAdd = async (newDocument) => {
        await api.addDocument(newDocument, props.workspaceID)
        setSidebarData([])
        fetchDocs()
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
                   <ButtonAddDocument onSubmit={handleAdd}/>
                </Grid>
            </Grid>
        </>
    );
};

