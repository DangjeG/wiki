import BlockComponent from "../Components/Block";
import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";


export default function DocumentVersions(){
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
                version.add(api.getBlockData(block_id, version.commit_id))
            }
            catch (e){
                console.log(e)
            }
        }
        setBlocks(versions)
    }
    useEffect(() => {
        fetchVersions()
    }, []);

    return(blocks.map((block)=>{
            return <BlockComponent block={block} mode={"version"}/>
        })
    )
}