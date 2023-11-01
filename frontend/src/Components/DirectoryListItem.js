import React, { useState } from 'react';
import {ExpandLess, ExpandMore} from "@mui/icons-material";
import {Collapse, IconButton, List, ListItemButton} from "@mui/material";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";



export default function DirectoryListItem(props) {


    const [open, setOpen] = useState(false);

    const handleOpen = () => {
        setOpen(!open);
    };

    const handleClick = (data) => {
        props.onClick(data)
    }

    return (
        <>
            <React.Fragment>
            <ListItem button  onClick={() => handleClick(props.id)} >
                <ListItemText primary={props.title} />
                {props.children && (
                    <IconButton size="small" onClick={() => handleOpen()}>
                        {open ? <ExpandLess /> : <ExpandMore />}
                    </IconButton>
                )}
            </ListItem>
            {open && props.children && <List>{props.children}</List>}
        </React.Fragment>
        </>
    );
};