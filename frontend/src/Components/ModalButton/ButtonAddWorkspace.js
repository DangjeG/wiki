import Button from "@mui/material/Button";
import {Box, Tooltip} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import React, {useState} from "react";
import {Form, Modal} from "react-bootstrap";
import {api} from "../../Config/app.config";


export default function ButtonAddWorkspace({onSubmit}) {

    const [show, setShow] = useState(false);
    const [newWorkspace, setNewWorkspace] = useState("");

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const handleSubmit = async () => {
        handleClose()
        onSubmit(newWorkspace)
    }

    return (
        <>
            <Button sx={{border: 'none', outline: 'none'}}
                    variant="outlined" onClick={handleShow}>
                <Tooltip sx={{width: '10px', height: '10px'}}
                         title="Добавить проект"
                         placement="top"
                         arrow>
                    <AddIcon sx={{color: '#000000'}}/>
                </Tooltip>
            </Button>

            <Modal show={show} onHide={handleClose}
                   style={{
                       overflow: 'auto', width: '400px', height: '550px', position: 'absolute',
                       left: '50%',
                       top: '55%',
                       transform: 'translate(-50%, -50%)',
                       display: 'flex',
                       justifyContent: 'center',
                       alignItems: 'center',
                   }}>
                <Modal.Header>
                    <Modal.Title>Добавить проект</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Название</Form.Label>
                            <Form.Control value={newWorkspace}
                                          onChange={(event) => setNewWorkspace(event.target.value)}/>
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button id="base-button" variant="outlined" onClick={handleClose}>Закрыть</Button>
                    <Box sx={{marginLeft: '10px'}}></Box>
                    <Button id="accent-button" variant="contained" onClick={handleSubmit}>Сохранить</Button>
                </Modal.Footer>
            </Modal>
        </>
    )
}