import {styled} from "styled-components";
import UndoIcon from '@mui/icons-material/Undo';
import {IconButton} from "@mui/material";

const Container = styled.div`
  padding: 5px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  box-shadow: 2px 2px 5px rgba(2, 2, 2, .4);
  align-items: flex-start;
  border-radius: 10px;
`

const InfoBlock = styled.div`
  display: flex;
  flex-direction: column;
`

export const Version = ({version, onRollback}) => {


    const handleClickRollback = (event) => {
        event.stopPropagation();
        onRollback(version.object_id, version.commit_id)
    }

    return(
        <Container>
            <InfoBlock>
                <h5>{version.committer_user.username}</h5>
                <p>{version.created_at}</p>
            </InfoBlock>
            <IconButton onClick={handleClickRollback}>
                <UndoIcon/>
            </IconButton>
        </Container>
    )
}