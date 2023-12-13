import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {api} from "../../Config/app.config";
import DescriptionIcon from "@mui/icons-material/Description";
import TopicIcon from '@mui/icons-material/Topic';
import WorkspacesIcon from '@mui/icons-material/Workspaces';
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import {TreeView} from "@mui/x-tree-view/TreeView";
import DocumentTreeItem from "./DocumentTreeItem"
import DocumentTreeItemEditButton from "./Buttons/DocumentTreeItemEditButton";
import DocumentTreeItemMenuButton from "./Buttons/DocumentTreeItemMenuButton";
import NewDocumentButton from "./Buttons/NewDocumentButton";


export function Sidebar({workspaceID}){

    const [sidebarData, setSidebarData] = useState([]);
    const [workspace, setWorkspace] = useState([])
    let navigate = useNavigate()

    const fetchDocs = async () => {
        try {
            const documentTreeResponse = await api.getDocumentsTree(workspaceID)
            setSidebarData(documentTreeResponse)
            await fetchWorkspace()
            navigate(`/workspace/${workspaceID}/document/${documentTreeResponse[0].id}/view`)
        }
        catch (e){
            console.log(e)
        }
    };

    const fetchWorkspace = async () =>{
        try{
            const response = await api.getWorkspaceInfo(workspaceID)
            setWorkspace(response)
        }
        catch (e){
            console.log(e)
        }
    }

    useEffect(() => {
        fetchWorkspace()
        fetchDocs()
    }, []);



    const handleAdd = async (newDocument) => {
        await api.addDocument(newDocument, workspaceID)
        setSidebarData([])
        fetchDocs()
    }

    const handleClick = (id) => {
        navigate(`/workspace/${workspaceID}/document/${id}/view`)
    }

    const documentButtons = (
        <>
            <DocumentTreeItemEditButton onClickEdit/>
            <DocumentTreeItemMenuButton
                // onClickNewDocument={onClickNewDocument}
                // onClickRename={onClickRename}
                // onClickDelete={onClickDelete}
            />
        </>
    );

    const workspaceButtons = (
        <>
            <NewDocumentButton onSubmit={handleAdd}/>
        </>
    )

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
                // onClickNewDocument={handleNewDocument}
                // onClickRename={}
                // onClickDelete={}
                // onClickEdit
                buttons={documentButtons}
                onClick={() => handleClick(item.id)}
            >

                {getChildren(item.children)}
            </DocumentTreeItem>
        ));
    }

    return (
        <>
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
                    buttons={workspaceButtons}
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
                                onClick={() => handleClick(item.id)}
                                buttons={documentButtons}
                            >
                                {getChildren(item.children)}
                            </DocumentTreeItem>
                        )
                    })}
                </DocumentTreeItem>

            </TreeView>
        </>
    );
};
