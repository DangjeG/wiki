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
            <IconButton onMouseEnter={handleHistoryButtonClick}>
                <HistoryIcon/>
            </IconButton>
            <VersionList
                wikiObject={document}
                show={showVersions}
                onRollback={handleRollback}
                onMouseLeave={handleHistoryButtonClick}
            />
        </>
    )
}