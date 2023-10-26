import {api} from "../app.config";
import React from "react";
import {Modal, Button} from "react-bootstrap";


export default function Logout() {
    React.useEffect( () => {
        async function fetch(){
            const logout = await api.logout()
        }
        fetch()
    })
    return (
        <div
        className="modal show"
        style={{ display: 'block', position: 'initial' }}>
        <Modal.Dialog>
            <Modal.Header>
                <Modal.Title>Successful</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>You have successfully logged out of your account.</p>
            </Modal.Body>

            <Modal.Footer>
                <Button href={"/"} variant="primary">Go back</Button>
            </Modal.Footer>
        </Modal.Dialog>
    </div>)
}