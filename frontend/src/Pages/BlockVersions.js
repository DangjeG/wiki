import BlockComponent from "../Components/Block";
import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";
import {Modal} from "react-bootstrap";


export default function BlockVersions(props){
    const [blocks, setBlocks] = useState([]);
    const fetchVersions = async (block_id) => {
        let versionsInfo = []
        let versions = []
        try {
            versionsInfo = await api.getBlockVersions(block_id)
        }
        catch (e){
            console.log(e)
        }
        for (let version of versionsInfo){
            try {
                let ver = await api.getBlockData(block_id, version.commit_id)
                versions.push(ver)
                console.log(ver)
            }
            catch (e){
                console.log(e)
            }
        }
        setBlocks(versions)
        alert(versions.length)
    }
    useEffect(() => {
        fetchVersions(props.block.id)
    }, []);

    return(
        <div>
            {blocks.map((block)=>{
                return <BlockComponent onChange={()=>{}} block={block} mode={"version"}/>
            })}
        </div>
    )
}