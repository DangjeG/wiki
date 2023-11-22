import {Table} from "react-bootstrap";
import React, {useEffect, useState} from "react"
import {api} from "../Configs/app.config";
import {Box} from "@mui/system";
import {Tooltip} from "@mui/material";
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';


export default function OrganizationsTable() {

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getOrganizations();
                setOrganizations(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
    }, []);


    const [organizations, setOrganizations] = useState([]);
    const [show, setShow] = useState(false);

    const [name, setName] = useState();
    const [description, setDescription] = useState();
    const [access, setAccess] = useState();


    const handleSubmit = () => {
        Add()
        handleClose()
    }
    const handleClose = () => {

        setShow(false)
    };
    const handleShow = () => setShow(true);


    async function Add() {

        await api.addOrganizations(name, description, access)
        const fetchData = async () => {
            try {
                const response = await api.getOrganizations();
                setOrganizations(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
        setName("")
        setDescription("")
        setAccess("")
    }

    return (
        <div style={{display: 'flex'}}>

            <Box sx={{ container:'true', margin: '10px', padding: '50px 50px', background: '#cdf',  borderRadius: '10px', width:'100%'}}>
                <Table sx={{borderCollapse: 'collapse', width: '100%'}}>
                    <thead >
                    <tr key="header">
                        <th id="table-style">
                            <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                     title="Название группы"
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Название
                        </th>
                        <th  id="table-style">
                            <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                     title="Описание группы"
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Описание
                        </th>
                        <th  id="table-style">
                            <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                     title={<span><strong>FULL_ACCESS</strong> - будет описание.<br/>
                                            <strong>WEB_ONLY</strong> - будет описание.<br/>
                                            <strong>LOCKED</strong> - будет описание.
                                            </span>}
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Права доступа
                        </th>

                    </tr>
                    </thead>
                    <tbody>
                    {Array.from(organizations).map((organization) => (
                        <tr key={organization.name}>
                            <td  id="table-style" >{organization.name}</td>
                            <td  id="table-style">{organization.description}</td>
                            <td  id="table-style">{organization.access}</td>
                        </tr>))}
                    </tbody>
                </Table>

            </Box>
        </div>)
}