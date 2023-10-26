import React, {useEffect, useState} from "react";
import {api} from "../app.config";
import {Dropdown} from "react-bootstrap";


export default function Home(){

    const [workspaces, setWorkspaces] = useState([]);


    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getWorkspaces();
                setWorkspaces(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
    }, []);

    let d = []
    function getDocs(id){
        const fetchData = async () => {
            try {
                return await api.getDocumentsTree(id);
            } catch (error) {
                console.log(error)
                alert("gfh")
            }
        };
        d = fetchData()
    }

    function getBlocs(id){
        const fetchData = async () => {
            try {
                return await api.getBlocks(id);
            } catch (error) {
                console.log(error)

            }
        };
        fetchData().then((resp)=>{
            return resp
        }) ;

    }


    const dcs = (id) => {
        getDocs(id)
        return(Array.from(d).map((doc) =>
            <Dropdown drop={"end"}>
                <Dropdown.Toggle id="dropdown-basic">
                    {doc.title}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                    {doc.children !== null? cldrn(doc.children): <></>}
                    {blk(doc.id)}
                </Dropdown.Menu>
            </Dropdown>
        ))
    }

    const cldrn = (childrens) => {
        return(
            Array.from(childrens).map((doc) =>
            <Dropdown drop={"end"}>
                <Dropdown.Toggle id="dropdown-basic">
                    {doc.title}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                    {childrens !== null? cldrn(doc.children): <></>}
                    {blk(doc.id)}
                </Dropdown.Menu>
            </Dropdown>
        ))
    }

    const blk = (id) => {
        Array.from(getBlocs(id)).map((block) =>
            <Dropdown.Item>{block.id}</Dropdown.Item>
        )
    }


    return (
        <>
            {Array.from(workspaces).map((workspace) =>
                <Dropdown drop={"end"}>
                    <Dropdown.Toggle id="dropdown-basic">
                        {workspace.title}
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                        {dcs(workspace.id)}
                    </Dropdown.Menu>
                </Dropdown>
            )}
        </>

    )
}