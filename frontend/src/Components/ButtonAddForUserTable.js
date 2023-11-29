import React, {useState} from 'react';
import "../Styles/AdminTools.css";
import AddIcon from "@mui/icons-material/Add";
import {Box, Button, Checkbox, FormControlLabel, FormLabel, Radio, RadioGroup, Tooltip} from "@mui/material";
import {Form, Modal} from "react-bootstrap";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import {api} from "../Config/app.config";


export default function ButtonAddUser() {

    const [show, setShow] = useState(false);
    const [isSecondNameExist, setExist] = useState(true);
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [secondName, setSecondName] = useState("");
    const [responsibility, setResponsibility] = useState('');
    const [position, setPosition] = useState("")

    const handleClose = () => {
        setShow(false);
    };

    const handleShow = () => {
        setShow(true);
    };

    const handleCreate = () => {
        const fetchData = async () => {
            try {
                await api.createApprovedUser(email, username, firstName, lastName, secondName,position, responsibility)
            } catch (error) {
                console.log(error);
            }
        };
        fetchData()
        setShow(false);
    };

    return (
        <div>
            <Button id="button-add"
                    variant="outlined"
                    onClick={handleShow}>
                <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                         title="Добавить пользователя"
                         placement="top"
                         arrow>
                    <AddIcon sx={{color: '#000000'}}/>
                </Tooltip>
            </Button>
            <Modal show={show} onHide={handleClose}
                   style={{
                       overflow: 'auto', width: '400px', height: '500px', position: 'absolute',
                       left: '50%',
                       top: '50%',
                       transform: 'translate(-50%, -50%)',
                       display: 'flex',
                       justifyContent: 'center',
                       alignItems: 'center',
                   }}>
                <Modal.Header>
                    <Modal.Title>Добавить пользователя</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                onChange={(event) => setEmail(event.target.value)}
                                as="textarea"
                                rows={1}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Логин</Form.Label>
                            <Form.Control
                                onChange={(event) => setUsername(event.target.value)}
                                as="textarea"
                                rows={1}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Имя</Form.Label>
                            <Form.Control
                                onChange={(event) => setFirstName(event.target.value)}
                                as="textarea"
                                rows={1}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Фамилия</Form.Label>
                            <Form.Control
                                onChange={(event) => setLastName(event.target.value)}
                                as="textarea"
                                rows={1}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Отчество</Form.Label>
                            <Form.Control
                                onChange={(event) => setSecondName(event.target.value)}
                                disabled={isSecondNameExist}
                                required={!isSecondNameExist}
                                as="textarea"
                                rows={1}
                            />
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={!isSecondNameExist}
                                        onClick={() => {
                                            setExist(!isSecondNameExist);
                                            setSecondName("");
                                        }}
                                    />
                                }
                                label="Отчество существует"
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Должность</Form.Label>
                            <Form.Control
                                onChange={(event) => setPosition(event.target.value)}
                                as="textarea"
                                rows={1}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <FormLabel component="legend">Роль</FormLabel>
                            <RadioGroup aria-label="responsibility" value={responsibility}
                                        onChange={(event) => setResponsibility(event.target.value)}>
                                <FormControlLabel value="VIEWER" control={<Radio/>}
                                                  label={
                                                      <span>ЗРИТЕЛЬ
                                                          <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                                                   title="лох"
                                                                   placement="top"
                                                                   arrow>
                                                              <InfoOutlinedIcon/>
                                                          </Tooltip>
                                                      </span>
                                                  }/>
                                <FormControlLabel value="EDITOR" control={<Radio/>}
                                                  label={
                                                      <span>РЕДАКТОР
                                                          <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                                                   title="не лох"
                                                                   placement="top"
                                                                   arrow>
                                                              <InfoOutlinedIcon/>
                                                          </Tooltip>
                                                      </span>
                                                  }/>
                                <FormControlLabel value="ADMIN" control={<Radio/>}
                                                  label={
                                                      <span>АДМИН
                                                          <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                                                   title="крутой чел"
                                                                   placement="top"
                                                                   arrow>
                                                              <InfoOutlinedIcon/>
                                                          </Tooltip>
                                                      </span>
                                                  }/>
                            </RadioGroup>
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button id="base-button" variant="outlined" onClick={handleClose}>Закрыть</Button>
                    <Box sx={{marginLeft: '10px'}}></Box>
                    <Button id="accent-button" variant="contained" onClick={handleCreate}>Сохранить</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};