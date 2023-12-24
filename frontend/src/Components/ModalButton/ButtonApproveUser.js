import React, {useState} from 'react';
import "../../Styles/AdminTools.css";
import AddIcon from "@mui/icons-material/Add";
import {Box, Button, FormControlLabel, FormLabel, Radio, RadioGroup, Tooltip} from "@mui/material";
import {Form, Modal} from "react-bootstrap";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import {api} from "../../Config/app.config";


export default function ButtonApproveUser(props) {

    const [show, setShow] = useState(false);
    const [description, setDescription] = useState("")
    const [responsibility, setResponsibility] = useState('');

    const handleClose = () => {
        setShow(false);
    };

    const handleShow = () => {
        setShow(true);
    };

    const handleApprove = () => {
        const fetchData = async () => {
            try {
                await api.approveUser(props.username, responsibility, description)
            } catch (error) {
                console.log(error);
            }
        };
        fetchData()
        setShow(false)
    };

    return (
        <div>
            <Button id="button-add"
                    variant="outlined"
                    onClick={handleShow}>
                <Tooltip sx={{width: '8%', height: '-5%', marginBottom: '2%', marginRight: '1%'}}
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
                    <Modal.Title>Описание</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                onChange={(event) => setDescription(event.target.value)}
                                as="textarea"
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <FormLabel component="legend">Роль</FormLabel>
                            <RadioGroup aria-label="responsibility" value={responsibility}
                                        onChange={(event) => setResponsibility(event.target.value)}>
                                <FormControlLabel value="VIEWER" control={<Radio/>}
                                                  label={
                                                      <span>ЗРИТЕЛЬ
                                                          <Tooltip sx={{
                                                              width: '15%',
                                                              marginBottom: '4%',
                                                              marginLeft: '3%',
                                                              color: '#3b3f42'
                                                          }}
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
                                                          <Tooltip sx={{
                                                              width: '15%',
                                                              marginBottom: '4%',
                                                              marginLeft: '3%',
                                                              color: '#3b3f42'
                                                          }}
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
                                                          <Tooltip sx={{
                                                              width: '15%',
                                                              marginBottom: '4%',
                                                              marginLeft: '3%',
                                                              color: '#3b3f42'
                                                          }}
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
                    <Button id="accent-button" variant="contained" onClick={handleApprove}>Сохранить</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};