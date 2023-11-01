import React, { useEffect, useState } from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import {Collapse, Grid} from "@mui/material";
import {ExpandLess, ExpandMore} from "@mui/icons-material";

const Sidebar = () => {
    const [sidebarData, setSidebarData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {

        };
        fetchData();
    }, []);

    const handleClick = () => {

    }
    function getChildren(childrens) {
        if (childrens.size() === 0) return null

        return (
            <>

            </>
        )
    }

    return (
         <Drawer
            open={true}
            onClose={handleClick}
            anchor="left"
            sx={{
                width: '20%', // Установите ширину боковой панели на 20% от родительского контейнера
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: '20%', // Установите ширину содержимого боковой панели на 20% от родительского контейнера
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

            </List>
                </Grid>
            </Grid>
        </Drawer>
    );
};

export default Sidebar;
