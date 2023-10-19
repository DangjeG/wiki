import {Table} from "react-bootstrap";
import {api} from "../app.config";
import React, {useEffect, useState} from "react";


export default function UsersTable() {


    const [users, setUsers] = useState([]);


    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getUsers();
                setUsers(response);
            } catch (error) {
                console.log(error)
            }

        };
        fetchData();
    }, []);



    return (
        <div style={{"padding": "50px 150px"}}>
            <Table>
                <thead>
                <tr>
                    <th>Email</th>
                    <th>Username</th>
                    <th>Full name</th>
                    <th>Responsibility</th>
                </tr>
                </thead>
                <tbody>
                {Array.from(users).map((user) => (
                    <tr>
                        <td>{user.email}</td>
                        <td>{user.username}</td>
                        <td>{user.first_name + " " + user.last_name + " " + user.second_name}</td>
                        <td>{user.responsibility}</td>
                    </tr>
                ))}
                </tbody>
            </Table>
        </div>
    )
}