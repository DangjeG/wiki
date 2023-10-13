import React, {useState} from "react";
import {Button, Form} from "react-bootstrap";
import "../Styles/Login.css"
import {api} from "../app.config";


export default function Login(){

    const [email, setEmail] = useState("");
    async function handleFormSubmit(event) {
        event.preventDefault();
        try {
            await api.login(email)
            window.location.href = '/verify';
        } catch (error) {
            console.error(error);
        }
    }
    return(
        <div className="login-form">
            <Form onSubmit={handleFormSubmit}>
                <Form.Group className="mb-3">
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