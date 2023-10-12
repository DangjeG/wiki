import React, {useState} from "react";
import {Button, Form} from "react-bootstrap";
import "../Styles/Login.css"
import {instance} from "../api.config";

export default function SignUp() {

    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [first_name, setFirstName] = useState("");
    const [last_name, setLastName] = useState("");
    const [second_name, setSecondName] = useState("");
    const [is_user_agreement_accepted, setAgreements] = useState(false);
    const [is_second_name_exist, setExist] = useState(true);
    async function handleFormSubmit(event) {
        event.preventDefault();
        try {
            const response = await instance.post(`/auth/signup`,
                {
                    "email" : email,
                    "username" : username,
                    "first_name" : first_name,
                    "last_name" : last_name,
                    "second_name" : second_name,
                    "is_user_agreement_accepted" : is_user_agreement_accepted,
                    "organization_id" : "3fa85f64-5717-4562-b3fc-2c963f66afa6"

                })
            const token = response.data.verify_token;
            localStorage.setItem('verify', token);
            window.location.href = '/verify';
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <div className="color-overlay d-flex justify-content-center align-content-center">
            <Form className="login-form" onSubmit={handleFormSubmit}>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="name@example.com"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="example_username"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>First name</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Иванов"
                        value={first_name}
                        onChange={(event) => setFirstName(event.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Last name</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Иван"
                        value={last_name}
                        onChange={(event) => setLastName(event.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Second name</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Иванович"
                        value={second_name}
                        onChange={(event) => setSecondName(event.target.value)}
                        disabled={is_second_name_exist}
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Check
                        variant="outline-primary"
                        inline
                        label="second name exist"
                        type="checkbox"
                        isValid={is_second_name_exist}
                        onClick={()=>{
                            setExist(!is_second_name_exist);
                            setSecondName("");
                        }}
                    />
                    <Form.Check
                        variant="outline-primary"
                        inline
                        label=" accept user agreement"
                        type="checkbox"
                        isValid={is_user_agreement_accepted}
                        onClick={()=>setAgreements(!is_user_agreement_accepted)}
                    />
                </Form.Group>
                <Button type="submit" variant="outline-primary"> Verify </Button>
            </Form>
        </div>
    );

}