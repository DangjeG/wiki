import React, { useState } from "react";
import {Button, Form} from "react-bootstrap";
import "../Styles/Login.css"
import {instance} from "../api.config";

export default function Verify(){

    const [code, setCode] = useState("");

    async function handleFormSubmit(event) {
        event.preventDefault();
        try {
             await instance.post(`/auth/verify`,
                {
                "token" : localStorage.getItem("verify"),
                "code": code
                }).then((resp)=>{
                localStorage.setItem('token', resp.data.access_token);
                window.location.href = '/';
            })
        } catch (error) {
            console.error(error);
        }
    }

    return(
        <div className="color-overlay d-flex justify-content-center align-content-center">
            <Form className="login-form" onSubmit={handleFormSubmit}>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Code from email</Form.Label>
                    <Form.Control
                        placeholder="EnterCode"
                        value={code}
                        onChange={(event) => setCode(event.target.value)}
                    />
                </Form.Group>
                <Button type="submit" variant="outline-primary"> Submit </Button>
            </Form>
        </div>
    )
}