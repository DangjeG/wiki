import React, {useEffect, useState} from 'react';
import "../Styles/AdminTools.css";
import AddIcon from "@mui/icons-material/Add";
import {Box, Button, Tooltip} from "@mui/material";
import {api} from "../Configs/app.config";
import {Form, Modal} from "react-bootstrap";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";


export default function ButtonAddOrganization() {

    const [show, setShow] = useState(false);
    const [name, setName] = useState();
    const [description, setDescription] = useState();
    const [access, setAccess] = useState();


    const handleSubmit = () => {
        handleClose()
    }
    const handleClose = () => {

        setShow(false)
    };
    const handleShow = () => setShow(true);



    return (
        <div>
            <Button id="button-add"
                    variant="outlined"
                    onClick={handleShow}>
                <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                         title="Добавить пользователя"
                         placement="top"
                         arrow>
                    <AddIcon sx={{color:'#000000'}}/>
                </Tooltip>
            </Button>
            <Modal show={show} onHide={handleClose}
                   style={{overflow: 'auto', width: '400px', height: '550px', position: 'absolute',
                       left: '50%',
                       top: '55%',
                       transform: 'translate(-50%, -50%)',
                       display: 'flex',
                       justifyContent: 'center',
                       alignItems: 'center',}}>
                <Modal.Header>
                    <Modal.Title>Добавить группу</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Название</Form.Label>
                            <Form.Control value={name} onChange={(event) => (setName(event.target.value))}/>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Описание</Form.Label>
                            <Form.Control value={description} onChange={(event) => (setDescription(event.target.value))}
                                          as="textarea" rows={3}/>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Check inline type="radio"
                                        label={
                                            <span>FULL_ACCESS
                                                          <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                                                   title="хз"
                                                                   placement="top"
                                                                   arrow>
                                                              <InfoOutlinedIcon />
                                                          </Tooltip>
                                                      </span>
                                        }
                                        name={"group"}
                                        onClick={() => setAccess("FULL_ACCESS")}/>
                            <Form.Check inline type="radio"
                                        label={
                                            <span>WEB_ONLY
                                                          <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                                                   title="хз"
                                                                   placement="top"
                                                                   arrow>
                                                              <InfoOutlinedIcon />
                                                          </Tooltip>
                                                      </span>
                                        }
                                        name={"group"}
                                        onClick={() => setAccess("WEB_ONLY")}/>
                            <Form.Check inline type="radio"
                                        label={
                                            <span>LOCKED
                                                          <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                                                   title="хз"
                                                                   placement="top"
                                                                   arrow>
                                                              <InfoOutlinedIcon />
                                                          </Tooltip>
                                                      </span>
                                        }
                                        name={"group"}
                                        onClick={() => setAccess("LOCKED")}/>
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button id="base-button" variant="outlined" onClick={handleClose}>Закрыть</Button>
                    <Box sx={{ marginLeft: '10px' }}></Box>
                    <Button id="accent-button" variant="contained" onClick={handleSubmit}>Сохранить</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );

}