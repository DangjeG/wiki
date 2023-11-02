import React, { useState } from "react";
import {Button, Form} from "react-bootstrap";
import "../Styles/Login.css"
import {api} from "../app.config";


export default function Verify(){

    const [code, setCode] = useState();

    async function handleFormSubmit(event) {
        event.preventDefault();
        try {
             await api.verify(code);
            window.location.href = '#';
            }
            catch (err){
            console.log(err)
            }
    }

    return(
        <div className="login-form">
            <Form onSubmit={handleFormSubmit}>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Code from email</Form.Label>
                    <Form.Control
                        placeholder="EnterCode"
                        value={code}
                        onChange={(event) => setCode(event.target.value)}
                    />
                </Form.Group>
                <Button id="button-with-border" type="submit" variant="outline-primary"> Submit </Button>
            </Form>
        </div>
    )
}