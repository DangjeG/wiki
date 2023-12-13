import {Box, IconButton} from "@mui/material";
import PostAddIcon from '@mui/icons-material/PostAdd';
import React, {useState} from "react";
import {Form, Modal} from "react-bootstrap";
import Button from "@mui/material/Button";


function NewDocumentButton({onSubmit}) {
    const [show, setShow] = useState(false);
    const [newDocument, setNewDocument] = useState()
    const handleClose = () => setShow(false)
    const handleShow = (event) => {
        event.stopPropagation();  // чтобы при нажатии на кнопку дерево не сворячивалось
        setShow(true)
    };
    const handleAdd = async () => {
        handleClose()
        onSubmit(newDocument)
    }

    return (
        <>
            <IconButton onClick={handleShow}>
                <PostAddIcon />
            </IconButton>

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

export default NewDocumentButton;
