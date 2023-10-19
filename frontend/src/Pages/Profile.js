import React, {useEffect, useState} from "react";
import {User} from "../Models/User";
import {api} from "../app.config";
import {ListGroup} from "react-bootstrap";


export default function Profile(){

    const [user, setUser] = useState(new User())

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getMe();
                setUser(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
    }, []);

    function getApproved(){
        if(user.responsibility !=="") return <ListGroup.Item style={{color: "lightgreen"}}>You are approved</ListGroup.Item>
        else return <ListGroup.Item style={{color: "red"}}>You are not approved</ListGroup.Item>
    }

    return(
        <div className="login-form">
            <ListGroup>
                <ListGroup.Item>Email: {user.email}</ListGroup.Item>
                <ListGroup.Item>Username: {user.username}</ListGroup.Item>
                <ListGroup.Item>Full name: {user.last_name + " " + user.first_name + " " + user.second_name}</ListGroup.Item>
                {getApproved()}
            </ListGroup>
        </div>
    )
}