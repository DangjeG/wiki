import {Navigate, Outlet} from "react-router-dom";


export default function ProtectedRoute({ requirement }){
    return requirement ? <Outlet /> : <Navigate to="/login" />;
}