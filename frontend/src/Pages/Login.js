import React, {useState} from "react";
import {Button, Form} from "react-bootstrap";
import "../Styles/Login.css"
import {instance} from "../api.config";


export default function Login(){

    const [email, setEmail] = useState("");
    async function handleFormSubmit(event) {
        event.preventDefault();
        try {
            const response = await instance.post(`/auth/login`, {"email": email})
            const token = response.data.verify_token;
            localStorage.setItem('verify', token);
            window.location.href = '/verify';
        } catch (error) {
            console.error(error);
        }
    }
    return(
        <div className="color-overlay d-flex justify-content-center align-content-center">
            <Form className="login-form" onSubmit={handleFormSubmit}>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="name@example.com"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                    />
                </Form.Group>
                <Button type="submit" variant="outline-primary"> Verify </Button>
            </Form>
        </div>
    );
}