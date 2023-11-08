import React, { useState } from "react";
import {Button, FormControl, InputLabel, Input, Typography, TextField, styled} from "@mui/material";
import { api } from "../Configs/app.config";
import "../Styles/Login.css";
import "../Styles/BaseColors.css";

const CustomTextField = styled(TextField)({
    '& .MuiInputLabel-root.Mui-focused': {
        display: 'none', // Скрываем заголовок при активном поле ввода
    },
});

export default function Login() {
    const [email, setEmail] = useState("");

    const handleInputChange = (event) => {
        setEmail(event.target.value);
    };

    async function handleFormSubmit(event) {
        event.preventDefault();
        try {
            await api.login(email);
            window.location.href = "#verify";
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <div id="login" className="login-form">
            <div>
                <Typography component="h2" variant="h6">
                    Email
                </Typography>
                <form onSubmit={handleFormSubmit}>
                    <FormControl fullWidth id="text-field">
                        <InputLabel htmlFor="email-input"
                                    style={{ visibility: email === '' ? 'visible' : 'hidden' }}
                        >
                            name@example.com
                        </InputLabel>
                        <CustomTextField fullWidth
                                         variant="outlined"
                                         type="email"
                                         value={email}
                                         onChange={handleInputChange}/>
                    </FormControl>
                    <Button id="accent-button" variant="outlined" type="submit">
                        ОТПРАВИТЬ КОД
                    </Button>
                </form>
            </div>
        </div>
    );
}