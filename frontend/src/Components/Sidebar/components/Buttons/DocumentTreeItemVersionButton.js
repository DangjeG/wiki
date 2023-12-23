import {IconButton} from "@mui/material";
import HistoryIcon from "@mui/icons-material/History";
import React, {useState} from "react";
import {VersionList} from "../VersionList";

export const DocumentTreeItemVersionButton = ({document, onRollback}) => {
    const [showVersions, setShowVersions] = useState(false)

    const handleRollback = () => {
        onRollback()
    }
    const handleHistoryButtonClick = (event) => {
        event.stopPropagation();
        setShowVersions(!showVersions)
    }

    return (
        <>
            <IconButton onClick={handleHistoryButtonClick}>
                <HistoryIcon/>
            </IconButton>
            <VersionList document={document} show={showVersions} onRollback={handleRollback}/>
        </>
    )
}