
import {Route, Routes} from "react-router-dom";
import WorkspaceDocs from "./WorkspaceDocs";
import WorkspaceSelect from "./WorkspaceSelect";





export default function Workspace(){
    return (
        <Routes>
            <Route path="/" element={<WorkspaceSelect/>} />
            <Route path="/:wp_id/*" element={<WorkspaceDocs/>} />
        </Routes>
    )
}