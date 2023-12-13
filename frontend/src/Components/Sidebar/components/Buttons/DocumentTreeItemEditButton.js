import {IconButton} from "@mui/material";
import {Edit as EditIcon} from "@mui/icons-material";
import React from "react";

const DocumentTreeItemEditButton = ({ onClick }) => {

    const handleClick = (event) => {
        event.stopPropagation();
        onClick()
    }

    return (
        <IconButton onClick={handleClick}>
            <EditIcon/>
        </IconButton>
    )
}

export default DocumentTreeItemEditButton;
