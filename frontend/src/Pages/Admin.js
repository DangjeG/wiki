import {Button, Table} from "react-bootstrap";
import {User} from "../Models/User";

export default function Admin() {

    let users = /*api.getUsers()*/ [
        new User("preikol@gmail.com", "User1" ,"Иванов", "Иван", "Иванович", "admin"),
        new User("hehe@gmail.com", "User2" ,"Петров", "Петр", "Петрович", "viewer"),
        new User("smeshno@gmail.com", "User3" ,"Приколов", "Прикол", "Приколович", "uzer")
    ]


    return (
        <div style={{"padding": "50px 150px"}}>
            <Table variant={"primary"}>
                <thead>
                <tr>
                    <th>Email</th>
                    <th>Username </th>
                    <th>Full name</th>
                    <th>Responsibility</th>
                </tr>
                </thead>
                <tbody>
                {Array.from(users).map((user) => (
                    <tr>
                        <td>{user.email}</td>
                        <td>{user.username}</td>
                        <td>{user.first_name + " "+ user.last_name + " "+ user.second_name}</td>
                        <td><Button> удалить все </Button></td>
                    </tr>
                ))}
                </tbody>
            </Table>
        </div>

    )
}