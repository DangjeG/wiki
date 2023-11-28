import React, { useState } from "react";
import {Button, FormControl, InputLabel, Input, Typography, TextField, styled} from "@mui/material";
import { api } from "../Config/app.config";
import "../Styles/Login.css";
import "../Styles/BaseColors.css";
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const CustomTextField = styled(TextField)({
    '& .MuiInputLabel-root.Mui-focused': {
        display: 'none', // Скрываем заголовок при активном поле ввода
    },
});

export default function Login() {
    const [email, setEmail] = useState("");
    const [isError, setIsError] = useState(false);
    const [errorText, setErrorText] = useState("")
    const handleInputChange = (event) => {
        setEmail(event.target.value);
    };

    async function handleFormSubmit(event) {
        event.preventDefault();
        try {
            await api.login(email);
            setIsError(false)
            window.location.href = "#verify";
        } catch (error) {
            setErrorText(error.response.data.message)
            setIsError(true)
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
                    {isError && (
                        <p style={{ color: 'red', fontFamily: 'Inter', fontSize: '11px' }}>
                            <ErrorOutlineIcon sx={{ height: '20px' }} /> {errorText}
                        </p>
                    )}
                    <Button id="accent-button" variant="outlined" type="submit">
                        ОТПРАВИТЬ КОД
                    </Button>
                </form>
            </div>
        </div>
    );
}