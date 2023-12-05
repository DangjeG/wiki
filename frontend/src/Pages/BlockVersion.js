import {Card} from "@mui/material";


export default function BlockVersion(props){
    return(
        <Card>
            <p>{props.date}</p>
            <p>{props.user}</p>
        </Card>
    )
}