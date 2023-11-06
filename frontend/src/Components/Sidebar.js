import React, {useEffect, useState} from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import {Grid} from "@mui/material";
import DirectoryListItem from "./DirectoryListItem";
import {api} from "../app.config";

export default function Sidebar(props){


    const [sidebarData, setSidebarData] = useState([]);



    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getDocumentsTree(props.workspaceID)
                setSidebarData(response)
            }
            catch (e){
                console.log(e)
            }
        };
        fetchData();
        if (sidebarData.length>0) props.onSelect(sidebarData[0].id)

    }, []);

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
         <Drawer
             open={props.open}
             onClose={props.onClose}
            anchor="left"
            sx={{
                width: '20%',
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: '20%',
                    boxSizing: 'border-box',
                },
                background: '#423e42'
            }}
        >
            <Grid
                container
                justifyContent="center"
                height="100%"
                sx={{background: '#423e42', color: '#ffdbee'}}
            >
                <Grid item>
             <List>
                 {getChildren(sidebarData)}
            </List>
                </Grid>
            </Grid>
        </Drawer>
    );
};

