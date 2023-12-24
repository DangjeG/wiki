import {styled} from "styled-components";
import UndoIcon from '@mui/icons-material/Undo';
import {IconButton, ListItem, ListItemText, Tooltip} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";

export const Version = ({version, onRollback}) => {



    const handleClickRollback = (event) => {
        event.stopPropagation();
        onRollback(version.object_id, version.commit_id)
    }


    const addLeadingZero = (number) => {
        if (number < 10) {
            return `0${number}`;
        }
        return number;
    }

    const getFormattedDate = (date) => {
        const year = date.getFullYear();
        const month = date.toLocaleString("default", { month: "short" });
        const day = date.getDate();
        const hours = date.getHours();
        const minutes = date.getMinutes();

        return `${addLeadingZero(hours)}:${addLeadingZero(minutes)} ${month} ${day}, ${year}`;
    }

    return (
        <ListItem onClick={handleClickRollback}>
            <EditIcon style={{"margin-right": "20px"}} />
            <Tooltip title="Нажмите для просмотра" arrow>
                <ListItemText
                    primary={`Кем изменино: ${version.committer_user.username}`}
                    secondary={getFormattedDate(new Date(version.created_at))} //"Jan 9, 2014"
                />
            </Tooltip>
            {/*<Tooltip title="Откатиться к версии" arrow>
                <IconButton onClick={handleClickRollback}>
                    <UndoIcon/>
                </IconButton>
            </Tooltip>*/}
        </ListItem>
    )
}