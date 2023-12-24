import "../Styles/Home.css"
import "../Styles/BaseColors.css"
import Button from '@mui/material/Button';
import {useNavigate} from "react-router-dom";

export default function Home({user}){

    let navigate = useNavigate()

    if (user !== null) {
        return (
            <div className="main-page">
                <p id="main-text">Добро пожаловать {user.username}</p>
                <Button id="accent-button"
                        onClick={() => {
                                navigate(`/workspace`)
                            }}>
                    НАЧАТЬ РАБОТУ
                </Button>
            </div>
        )
    }
    else {
        return (
            <div className="main-page">
                <p id="main-text">Менеджер вашего пространства</p>
                <Button id="accent-button"
                        onClick={() => {
                            navigate(`/login`)
                        }}>
                    ВОЙТИ
                </Button>
            </div>
        )
    }
}