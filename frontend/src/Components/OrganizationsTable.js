import {Button, Form, Modal, Table} from "react-bootstrap";
import {useEffect, useState} from "react"
import {api} from "../app.config";


export default function OrganizationsTable() {



    const [organizations, setOrganizations] = useState([]);

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



    const [name, setName] = useState();
    const [description, setDescription] = useState();
    const [access, setAccess] = useState();


    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
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

    return (<div style={{"padding": "50px 150px"}}>
        <Table>
            <thead>
            <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Access</th>

            </tr>
            </thead>
            <tbody>
            {Array.from(organizations).map((organization) => (<tr>
                <td>{organization.name}</td>
                <td>{organization.description}</td>
                <td>{organization.access}</td>
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
                <Button variant="primary" onClick={() => {
                    Add()
                    handleClose()
                }}>
                    Save Changes
                </Button>
            </Modal.Footer>
        </Modal>
        <Button variant="light" onClick={handleShow}>+</Button>
    </div>)

}