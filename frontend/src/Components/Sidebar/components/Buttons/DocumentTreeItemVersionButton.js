import {IconButton} from "@mui/material";
import HistoryIcon from "@mui/icons-material/History";
import React, {useState} from "react";
import {VersionList} from "../VersionList";

export const DocumentTreeItemVersionButton = ({document, onRollback}) => {
    const [showVersions, setShowVersions] = useState(false)

    const handleRollback = (doc_id, commit_id) => {
        onRollback(doc_id, commit_id)
    }
    const handleHistoryButtonClick = (event) => {
        event.stopPropagation();
        setShowVersions(!showVersions)
    }

    const listStyles = {
        background: "white",
        "border-radius": "10px",
        "max-height": "300px",
        "min-height": "10px",
        "min-width": "300px",
        overflow: "auto",
        position: "absolute",
        "z-index": "100"
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
                listStyles={listStyles}
            />
        </>
    )
}