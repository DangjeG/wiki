
import {Route, Routes} from "react-router-dom";
import WorkspaceDocs from "./WorkspaceDocs";
import WorkspaceSelect from "./WorkspaceSelect";
import {useState} from "react";




export default function Workspace(){

    const [workspaceID, setWorkspaceID] = useState("");

    return (
        <Routes>
            <Route path="/docs" element={<WorkspaceDocs workspace_id={workspaceID} />} />
            <Route path="/select" element={<WorkspaceSelect onSelect={setWorkspaceID}/>} />
        </Routes>
    )
}