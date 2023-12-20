import React, {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import {api} from "../../Config/app.config";
import DescriptionIcon from "@mui/icons-material/Description";
import TopicIcon from '@mui/icons-material/Topic';
import WorkspacesIcon from '@mui/icons-material/Workspaces';
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import {TreeView} from "@mui/x-tree-view/TreeView";
import DocumentTreeItem from "./components/DocumentTreeItem"
import DocumentTreeItemEditButton from "./components/Buttons/DocumentTreeItemEditButton";
import DocumentTreeItemMenuButton from "./components/Buttons/DocumentTreeItemMenuButton";
import NewDocumentButton from "./components/Buttons/NewDocumentButton";
import {CircularProgress} from "@mui/material";
import ButtonAddDocument from "../ModalButton/ButtonAddDocument";
import PostAddIcon from "@mui/icons-material/PostAdd";


export function Sidebar(){

    const [docsLoad, setDocsLoad] = useState(true);
    const [wpLoad, setWpLoad] = useState(true);
    const [sidebarData, setSidebarData] = useState([]);
    const [workspace, setWorkspace] = useState(null)
    let navigate = useNavigate()
    let {wp_id, mode} = useParams();


    useEffect(() => {

        setDocsLoad(true)
        setWpLoad(true)
        fetchWorkspace(wp_id)
        fetchDocs(wp_id)
    }, []);


    useEffect(() => {
        setDocsLoad(true)
        setWpLoad(true)
        fetchDocs(wp_id)
        fetchWorkspace(wp_id)
    }, [wp_id]);

    const fetchDocs = async (workspaceID) => {
        try {
            const response = await api.getDocumentsTree(workspaceID)
            setSidebarData(response)
            console.log(sidebarData)
            setDocsLoad(false)
        }
        catch (e){
            console.log(e)
        }
    };

    const fetchWorkspace = async (workspaceID) =>{
        try{
            const response = await api.getWorkspaceInfo(workspaceID)
            setWorkspace(response)
            setWpLoad(false)
        }
        catch (e){
            console.log(e)
        }
    }

    const handleAdd = async (newDocument, parent_id) => {
        await api.addDocument(newDocument, wp_id, parent_id)
        setSidebarData([])
        fetchDocs(wp_id)
    }

    const handleDelete = async (document_id) => {
        await api.deleteDoc(document_id)
        setSidebarData([])
        fetchDocs(wp_id)
    }

    const handleExport = async (document_id, filename) => {
        await api.exportDoc(document_id, filename)
    }

    const handleClick = (id, mode) => {
        navigate(`/workspace/${wp_id}/document/${id}/${mode}`)
    }

    function getChildren(children) {
        if (children === null) return null
        return children.map((item) => (
            <DocumentTreeItem
                nodeId={item.id}
                labelText={item.title}
                labelIcon={item.children ? TopicIcon : DescriptionIcon}
                color="#1a73e8"
                bgColor="#e8f0fe"
                colorForDarkMode="#B8E7FB"
                bgColorForDarkMode="#071318"
                buttons={(
                    <>
                        <DocumentTreeItemEditButton onClick={() => handleClick(item.id, "edit")}/>
                        <DocumentTreeItemMenuButton
                             onClickNewDocument={(title) => handleAdd(title, item.id)}
                             onClickDelete={() => handleDelete(item.id)}
                             onClickExport={() => handleExport(item.id, item.title)}
                        />
                    </>
                )}
                onClick={() => handleClick(item.id, "view")}
            >

                {getChildren(item.children)}
            </DocumentTreeItem>
        ));
    }

    return (
        <>
            {wpLoad || docsLoad? <CircularProgress /> :
                <TreeView
                    defaultCollapseIcon={<ExpandMoreIcon />}
                    defaultExpandIcon={<ChevronRightIcon />}
                >
                    <DocumentTreeItem
                        nodeId={workspace.id}
                        labelText={workspace.title}
                        labelFontWeight={900}
                        labelIcon={WorkspacesIcon}
                        color="#1a73e8"
                        bgColor="#e8f0fe"
                        colorForDarkMode="#B8E7FB"
                        bgColorForDarkMode="#071318"
                        buttons={
                        (
                            <>
                                <ButtonAddDocument onSubmit={handleAdd}>
                                    <PostAddIcon />
                                </ButtonAddDocument>
                            </>
                        )}
                    >
                        {sidebarData.map((item) =>
                        {
                            return (
                                <DocumentTreeItem
                                    nodeId={item.id}
                                    labelText={item.title}
                                    labelIcon={item.children ? TopicIcon : DescriptionIcon}
                                    color="#1a73e8"
                                    bgColor="#e8f0fe"
                                    colorForDarkMode="#B8E7FB"
                                    bgColorForDarkMode="#071318"
                                    onClick={() => handleClick(item.id, "view")}
                                    buttons={(
                                        <>
                                            <DocumentTreeItemEditButton onClick={() => handleClick(item.id, "edit")}/>
                                            <DocumentTreeItemMenuButton
                                                 onClickNewDocument={(title) => handleAdd(title, item.id)}
                                                 onClickDelete={() => handleDelete(item.id)}
                                                 onClickExport={() => handleExport(item.id,  item.title)}
                                            />
                                        </>
                                    )}
                                >
                                    {getChildren(item.children)}
                                </DocumentTreeItem>
                            )
                        })}
                    </DocumentTreeItem>

                </TreeView>}
        </>
    );
}
