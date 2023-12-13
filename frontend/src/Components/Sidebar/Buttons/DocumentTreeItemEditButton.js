import {IconButton} from "@mui/material";
import {Edit as EditIcon} from "@mui/icons-material";
import React from "react";

const DocumentTreeItemEditButton = ({ onClick }) => (
    <IconButton onClick={onClick}>
        <EditIcon />
    </IconButton>
);

export default DocumentTreeItemEditButton;
