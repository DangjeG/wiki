import {Nav} from "react-bootstrap";
import {useState} from "react";
import UsersTable from "../Components/UsersTable";
import OrganizationsTable from "../Components/OrganizationsTable";

export default function Admin() {

    const [table, setTable] = useState(<UsersTable/>);

    const handleSelect = (eventKey) => {
        switch (eventKey){
            case "users":
                setTable(<UsersTable/>)
                break
            case "organizations":
                setTable( <OrganizationsTable/>)
                break
        }
    };


    return (
        <>
            <Nav variant="underlin" defaultActiveKey="users" onSelect={handleSelect}>
                <Nav.Item>
                    <Nav.Link  eventKey="users">Users</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                    <Nav.Link eventKey="organizations">Organizations</Nav.Link>
                </Nav.Item>
            </Nav>
            {table}
        </>
    )
}