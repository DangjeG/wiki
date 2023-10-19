import React, {useEffect, useState} from "react";
import {Button, Form} from "react-bootstrap";
import "../Styles/Login.css"
import {api} from "../app.config";


export default function SignUp() {

    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [first_name, setFirstName] = useState("");
    const [last_name, setLastName] = useState("");
    const [second_name, setSecondName] = useState("");
    const [organizationId, setOrganizationId] = useState("");
    const [is_user_agreement_accepted, setAgreements] = useState(false);
    const [is_second_name_exist, setExist] = useState(true);
    const [organizations, setOrganizations] = useState([]);


    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getOrganizations();
                setOrganizations(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
    }, []);


    async function handleFormSubmit(event) {
        event.preventDefault();

        try {
            await api.signup(email, username, first_name, last_name, second_name, organizationId, is_user_agreement_accepted)
            window.location.href = '/verify';
        } catch (error) {
            console.error(error);
        }
    }


    return (
        <div className="login-form">

            <Form onSubmit={handleFormSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="name@example.com"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="example_username"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>First name</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Иванов"
                        value={first_name}
                        onChange={(event) => setFirstName(event.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3" >
                    <Form.Label>Last name</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Иван"
                        value={last_name}
                        onChange={(event) => setLastName(event.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3" >
                    <Form.Label>Second name</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Иванович"
                        value={second_name}
                        onChange={(event) => setSecondName(event.target.value)}
                        disabled={is_second_name_exist}
                    />
                </Form.Group>
                <Form.Group>
                    <Form.Label>Organization</Form.Label>
                    <Form.Select onChange={(e) => setOrganizationId(e.currentTarget.value)}>
                        {Array.from(organizations).map((organization) => (
                            <option value={organization.id}>{organization.name}</option>
                        ))}
                    </Form.Select>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Check
                        inline
                        label="second name exist"
                        type="checkbox"
                        onClick={()=>{
                            setExist(!is_second_name_exist);
                            setSecondName("");
                        }}/>
                    <Form.Check
                        inline
                        label="accept user agreement"
                        type="checkbox"
                        onClick={()=> {
                            setAgreements(!is_user_agreement_accepted)
                        }}/>
                </Form.Group>
                <Button type="submit" variant="outline-primary"> Verify </Button>
            </Form>
        </div>
    );

}