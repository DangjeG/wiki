import {Button, Form, Modal, Table} from "react-bootstrap";
import {useEffect, useState} from "react"
import {api} from "../app.config";
import {Box} from "@mui/system";


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
        <div style={{"padding": "10px 70px", margin: '20px', background: '#d4b0ce',  borderRadius: '8px'}}>
            <Box sx={{width: '100%', margin: '10px', padding: '50px 50px', background: '#d4b0ce',  borderRadius: '8px'}}>
                <Table style={{background: '#d4b0ce'}}>
                    <thead >
                    <tr key="header">
                        <th style={{ background: '#d4b0ce', border: 'none' }}>Name</th>
                        <th style={{ background: '#d4b0ce', border: 'none' }}>Description</th>
                        <th style={{ background: '#d4b0ce', border: 'none' }}>Access</th>

                    </tr>
                    </thead>
                    <tbody>
                    {Array.from(organizations).map((organization) => (
                        <tr key={organization.name}>
                            <td style={{ background: '#d4b0ce', border: 'none' }}>{organization.name}</td>
                            <td style={{ background: '#d4b0ce', border: 'none' }}>{organization.description}</td>
                            <td style={{ background: '#d4b0ce', border: 'none' }}>{organization.access}</td>
                        </tr>))}
                    </tbody>
                </Table>
                <Modal show={show} onHide={handleClose}>
                    <Modal.Header>
                        <Modal.Title>Add organization</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group className="mb-3">
                                <Form.Label>Name</Form.Label>
                                <Form.Control value={name} onChange={(event) => (setName(event.target.value))}/>
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>Description</Form.Label>
                                <Form.Control value={description} onChange={(event) => (setDescription(event.target.value))}
                                              as="textarea" rows={3}/>
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Check inline type="radio" label={`FULL_ACCESS`} name={"group"}
                                            onClick={() => setAccess("FULL_ACCESS")}/>
                                <Form.Check inline type="radio" label={`WEB_ONLY`} name={"group"}
                                            onClick={() => setAccess("WEB_ONLY")}/>
                                <Form.Check inline type="radio" label={`LOCKED`} name={"group"}
                                            onClick={() => setAccess("LOCKED")}/>
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}>
                            Close
                        </Button>
                        <Button variant="primary" onClick={handleSubmit}>
                            Save Changes
                        </Button>
                    </Modal.Footer>
                </Modal>
                <Button style={{ background: '#bd97b6', border: 'none' }} variant="light" onClick={handleShow}>+</Button>
            </Box>
        </div>)
}