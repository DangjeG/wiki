import {styled} from "styled-components";
import {api} from "../../../Config/app.config";
import {useEffect, useState} from "react";
import {Version} from "./Version";

const Container = styled.div`
  background: white;
  position: absolute;
  display: flex;
  flex-direction: column;
  z-index: 100;
  width: 10px;
  min-width: 300px;
  min-height: 10px;
  border-radius: 10px;
  gap: 5px;
`

export const VersionList = ({document, show, onRollback}) => {


    const [versions, setVersions] = useState([])
    const fetchVersions = async () =>{
        try {
            setVersions([])
            const res = await api.getDocVersions(document.id)
            setVersions(res)
        }
        catch (e){
            console.log(e)
        }

    }

    const handleRollback = async (document_id, commit_id) => {
        await api.rollbackDoc(document_id, commit_id)
        onRollback()
        fetchVersions()
    }
    
    useEffect(() => {
        fetchVersions()

    }, [])

    if (show)
        return(
            <Container>
                {versions.map((item) =>{
                    return <Version version={item} onRollback={handleRollback}/>
                })}
            </Container>
    )
    else
        return null
}