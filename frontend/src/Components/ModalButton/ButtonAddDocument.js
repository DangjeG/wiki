import {Form, Modal} from "react-bootstrap";
import Button from "@mui/material/Button";
import {Box, Tooltip} from "@mui/material";
import React, {useState} from "react";
import AddIcon from "@mui/icons-material/Add";


export default function ButtonAddDocument({onSubmit, children},){

    const [show, setShow] = useState(false);
    const [newDocument, setNewDocument] = useState()
    const handleClose = () => setShow(false)
    const handleShow = () => setShow(true);
    const handleAdd = async () => {
        handleClose()
        onSubmit(newDocument)
    }

    return(
        <>
            <div onClick={handleShow}>
                {children}
            </div>

            <Modal show={show} onHide={handleClose}
                   style={{overflow: 'auto', width: '400px', height: '550px', position: 'absolute',
                       left: '50%',
                       top: '55%',
                       transform: 'translate(-50%, -50%)',
                       display: 'flex',
                       justifyContent: 'center',
                       alignItems: 'center',}}>
                <Modal.Header>
                    <Modal.Title>Добавить документ</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Название</Form.Label>
                            <Form.Control value={newDocument} onChange={(event) => setNewDocument(event.target.value)} />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button id="base-button" variant="outlined" onClick={handleClose}>Закрыть</Button>
                    <Box sx={{ marginLeft: '10px' }}></Box>
                    <Button id="accent-button" variant="contained" onClick={handleAdd}>Сохранить</Button>
                </Modal.Footer>
            </Modal>
        </>
    )
}