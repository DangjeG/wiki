import React, { useState } from 'react';
import { ListItem, ListItemText, IconButton, List, Collapse } from '@mui/material';
import { ExpandLess, ExpandMore, History, SaveAlt } from '@mui/icons-material';
import {api} from "../Config/app.config";

export default function DirectoryListItem(props) {

    const [open, setOpen] = useState(false);
    const [showHistoryDialog, setShowHistoryDialog] = useState(false);
    const [versions, setVersions] = useState([])

    const fetchVersions = async () =>{
        try {
            const response = await api.getDocVersions(props.id)
            setVersions(response)
        }
        catch (e){
            console.log(e)
        }
    }

    const handleOpen = () => {
        setOpen(!open);
    };

    const handleClick = (data) => {
        props.onClick(data);
    }

    const handleShowHistory = (event) => {
        event.stopPropagation();
        setShowHistoryDialog(true);
    };

    const handleExport = (event) => {
        event.stopPropagation(); // Предотвращаем срабатывание основного onClick
        // Имплементируйте логику для экспорта
    };

    return (
        <>
            <ListItem button onClick={() => handleClick(props.id)}>
                <ListItemText primary={props.title} />
                {props.children && (
                    <IconButton size="small" onClick={handleOpen}>
                        {open ? <ExpandLess /> : <ExpandMore />}
                    </IconButton>
                )}
                <IconButton size="small" onClick={handleShowHistory}>
                    <History />
                </IconButton>
                <IconButton size="small" onClick={handleExport}>
                    <SaveAlt />
                </IconButton>
            </ListItem>
            {open && props.children && <List>{props.children}</List>}
            {/* Окно для истории, которое будет появляться при нажатии на кнопку */}
            {/* Вам нужно добавить логику и верстку этого окна */}
            {showHistoryDialog && (
                <div>
                    {versions.map((item)=>{
                        return <div style={{margin : "10px"}}>
                            <p>Created at: {item.created_at}</p>
                            <p>Creator: {item.committer_user.username}</p>
                        </div>
                    })}
                </div>
            )}
        </>
    );
};