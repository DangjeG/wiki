import React, { useEffect, useState } from "react";
import { Button, Checkbox, FormControl, FormControlLabel, InputLabel, MenuItem, Select, TextField, Typography } from "@mui/material";
import { api } from "../Config/app.config";
import "../Styles/Login.css";

export default function SignUp() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [secondName, setSecondName] = useState("");
    const [organizationId, setOrganizationId] = useState("");
    const [isUserAgreementAccepted, setAgreements] = useState(false);
    const [isSecondNameExist, setExist] = useState(true);
    const [organizations, setOrganizations] = useState([]);

    useEffect(() => {
    }, []);

    async function handleFormSubmit(event) {
        event.preventDefault();
        try {
            await api.signup(email, username, firstName, lastName, secondName, organizationId, isUserAgreementAccepted);
            window.location.href = "#verify";
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <div id="signup" className="login-form">
            <form onSubmit={handleFormSubmit}>
                <Typography component="h2" variant="h6">
                    Email
                </Typography>
                <TextField
                    type="email"
                    placeholder="name@example.com"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    fullWidth
                    margin="normal"
                    required
                    sx={{background:'#FFFFFF'}}
                />
                <Typography component="h2" variant="h6">
                    Логин
                </Typography>
                <TextField
                    type="text"
                    placeholder="example_username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    fullWidth
                    margin="normal"
                    required
                    sx={{background:'#FFFFFF'}}
                />
                <Typography component="h2" variant="h6">
                    Имя
                </Typography>
                <TextField
                    type="text"
                    placeholder="Иванов"
                    value={firstName}
                    onChange={(event) => setFirstName(event.target.value)}
                    fullWidth
                    margin="normal"
                    required
                    sx={{background:'#FFFFFF'}}
                />
                <Typography component="h2" variant="h6">
                    Фамилия
                </Typography>
                <TextField
                    type="text"
                    placeholder="Иван"
                    value={lastName}
                    onChange={(event) => setLastName(event.target.value)}
                    fullWidth
                    margin="normal"
                    required
                    sx={{background:'#FFFFFF'}}
                />
                <Typography component="h2" variant="h6">
                    Отчество
                </Typography>
                <TextField
                    type="text"
                    placeholder="Иванович"
                    value={secondName}
                    onChange={(event) => setSecondName(event.target.value)}
                    fullWidth
                    margin="normal"
                    disabled={isSecondNameExist}
                    required={!isSecondNameExist}
                    sx={{background:'#FFFFFF'}}
                />
                <FormControlLabel
                    control={
                        <Checkbox
                            checked={!isSecondNameExist}
                            onClick={() => {
                                setExist(!isSecondNameExist);
                                setSecondName("");
                            }}
                        />
                    }
                    label="Отчество существует"
                />
                <FormControlLabel
                    control={<Checkbox checked={isUserAgreementAccepted} onClick={() => setAgreements(!isUserAgreementAccepted)} />}
                    label="Принять пользовательское соглашение"
                />
                <Button  id="accent-button" variant="outlined" type="submit" fullWidth>
                    ОТПРАВИТЬ КОД
                </Button>
            </form>
        </div>
    );
}