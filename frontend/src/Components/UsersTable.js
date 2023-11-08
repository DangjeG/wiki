import React, { useEffect, useState } from 'react';
import { Box, Button,Table, Tooltip } from '@mui/material';
import { api } from "../Configs/app.config";
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import "../Styles/AdminTools.css";
import "../Styles/BaseColors.css"
import ButtonApproveUser from "./ButtonApproveUser";

export default function UsersTable() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getUsers();
                setUsers(response);
            } catch (error) {
                console.log(error);
            }
        };
        fetchData();
    }, []);


    return (
        <div style={{display: 'flex'}}>

            <Box sx={{ container:'true', margin: '10px', padding: '50px 50px', background: '#cdf',  borderRadius: '10px', width:'100%'}}>
                <Table sx={{borderCollapse: 'collapse', width: '100%'}}>
                    <thead>
                    <tr key="header">
                        <th  id="table-style">
                            <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                     title="email пользователя - его контактная почта, куда можно отправить код"
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Email
                        </th>
                        <th  id="table-style">
                            <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                     title="Логин используется пользователем для входа в систему"
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Логин
                        </th>
                        <th  id="table-style">
                            <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                     title="Фамилия, имя и отчество пользователя"
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            ФИО
                        </th>
                        <th  id="table-style">
                            <Tooltip sx={{width:'15px', height:'15px', marginBottom: '5px', marginRight:'5px'}}
                                     title={<span><strong>Зритель</strong> - будет описание.<br/>
                                            <strong>Редактор</strong> - будет описание.<br/>
                                            <strong>Админ</strong> - будет описание.
                                            </span>}
                                     placement="top"
                                     arrow>
                                <InfoOutlinedIcon />
                            </Tooltip>
                            Роль
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    {users.map((user) => (
                        <tr key={user.username}>
                            <td  id="table-style">{user.email}</td>
                            <td  id="table-style">{user.username}</td>
                            <td  id="table-style">{user.first_name + ' ' + user.last_name + ' ' + user.second_name}</td>
                            <td  id="table-style">
                                {user.wiki_api_client === null ? (
                                    <ButtonApproveUser username={user.username}/>
                                ) : (
                                    user.wiki_api_client.responsibility
                                )}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </Table>
            </Box>
        </div>
    );
}