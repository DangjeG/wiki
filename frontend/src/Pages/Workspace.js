
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
            <Route path="/docs" element={<WorkspaceDocs setHistoryBlock={handleSetBlockHistory} workspace_id={workspaceID} />} />
            <Route path="/select" element={<WorkspaceSelect onSelect={setWorkspaceID}/>} />
            <Route path="/block_history" element={<BlockVersions block={blockHistory}/>} />
        </Routes>
    )
}