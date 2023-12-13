import React from "react";
import {IconButton, Menu, MenuItem} from "@mui/material";
import {MoreVert as MoreVertIcon} from "@mui/icons-material";

const DocumentTreeItemMenuButton = ({ onClickNewDocument, onClickRename, onClickDelete, workspaceId, documentId }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleOpenMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleCloseMenu = () => {
        setAnchorEl(null);
    };

    return (
        <>
            <IconButton onClick={handleOpenMenu}>
                <MoreVertIcon />
            </IconButton>
            <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleCloseMenu}>
                <MenuItem onClick={() => onClickNewDocument()}>New Document</MenuItem>
                <MenuItem onClick={() => onClickRename()}>Rename</MenuItem>
                <MenuItem onClick={() => onClickDelete()}>Delete</MenuItem>
            </Menu>
        </>
    );
};

export default DocumentTreeItemMenuButton;
