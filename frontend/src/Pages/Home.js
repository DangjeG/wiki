import "../Styles/Home.css"
import "../Styles/BaseColors.css"
import Button from '@mui/material/Button';

export default function Home(){

   return (
       <div className="main-page">
          <p id="main-text">Менеджер вашего пространства</p>
          <Button id="accent-button"
                  href="#login">
             ВОЙТИ
          </Button>
       </div>
   )
}