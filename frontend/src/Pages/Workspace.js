
import {Route, Routes} from "react-router-dom";
import WorkspaceDocs from "./WorkspaceDocs";
import WorkspaceSelect from "./WorkspaceSelect";
import {useState} from "react";
import BlockVersions from "./BlockVersions";




export default function Workspace(){

    const [workspaceID, setWorkspaceID] = useState("");
    const [blockHistory, setBlockHistory] = useState(null)
    const handleSetBlockHistory = (block) => {
      setBlockHistory(block)
    }

    return (
        <Routes>
            <Route path="/" element={<WorkspaceSelect onSelect={setWorkspaceID}/>} />
            <Route path="/:wp_id/*" element={<WorkspaceDocs setHistoryBlock={handleSetBlockHistory} />} />
        </Routes>
    )
}