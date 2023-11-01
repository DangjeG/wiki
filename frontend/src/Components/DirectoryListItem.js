import React, { useState } from 'react';
import {ExpandLess, ExpandMore} from "@mui/icons-material";
import {Collapse, List, ListItemButton} from "@mui/material";
import ListItem from "@mui/material/ListItem";



export default function DirectoryListItem(props) {
    const [open, setOpen] = useState(false);

    const handleClick = () => {
        setOpen(!open);
    };

    return (
        <>
            <ListItem>
                Основной элемент списка
                {open ? <ExpandLess /> : <ExpandMore />}
            </ListItem>
            onClick={handleClick}
            <Collapse in={open} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                    {props.childrens}
                </List>
            </Collapse>
        </>
    );
};