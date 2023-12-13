import React, {useState} from "react";
import {Box, IconButton, Menu, MenuItem} from "@mui/material";
import {MoreVert as MoreVertIcon} from "@mui/icons-material";
import ButtonAddDocument from "../../../ModalButton/ButtonAddDocument";
import {Form, Modal} from "react-bootstrap";
import Button from "@mui/material/Button";

const DocumentTreeItemMenuButton = ({ onClickNewDocument, onClickRename, onClickDelete, workspaceId, documentId }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const [show, setShow] = useState(false);
    const [newDocument, setNewDocument] = useState()
    const handleClose = () => setShow(false)
    const handleShow = () => setShow(true);
    const handleAdd = async () => {
        handleClose()
        onClickNewDocument(newDocument)
    }

    const handleOpenMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleCloseMenu = () => {
        setAnchorEl(null);
    };

    return (
        <>
            <IconButton onClick={handleOpenMenu}>
                <MoreVertIcon />
            </IconButton>
            <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleCloseMenu}>
                <MenuItem onClick={() => {
                    setShow(true)
                    handleCloseMenu()
                }}>New Document</MenuItem>
                {/*<MenuItem onClick={() => onClickRename()}>Rename</MenuItem>*/}
                <MenuItem onClick={() => {
                    onClickDelete()
                    handleCloseMenu()
                }}>Delete</MenuItem>
            </Menu>

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
    );
};

export default DocumentTreeItemMenuButton;
