import React from "react";
import {useTheme} from "@mui/material/styles";
import {Box, Typography} from "@mui/material";
import DocumentTreeItemEditButton from "./Buttons/DocumentTreeItemEditButton"
import DocumentTreeItemMenuButton from "./Buttons/DocumentTreeItemMenuButton"
import DocumentTreeItemRoot from "./DocumentTreeItemRoot";


const DocumentTreeItem = React.forwardRef(function StyledTreeItem(props, ref) {
    const theme = useTheme();
    const {
        bgColor,
        color,
        labelIcon: LabelIcon,
        labelInfo,
        labelText,
        labelFontWeight,
        colorForDarkMode,
        bgColorForDarkMode,
        // onClickNewDocument,
        // onClickRename,
        // onClickDelete,
        // onClickEdit,
        buttons,
        ...other
    } = props;

    const styleProps = {
        '--tree-view-color': theme.palette.mode !== 'dark' ? color : colorForDarkMode,
        '--tree-view-bg-color':
            theme.palette.mode !== 'dark' ? bgColor : bgColorForDarkMode,
    };

    return (
        <DocumentTreeItemRoot
            label={
                <Box
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                        p: 0.5,
                        pr: 0,
                    }}
                >
                    <Box component={LabelIcon} color={labelFontWeight ? "black" : "inherit"} sx={{ mr: 1 }} />
                    <Typography variant="body2"
                                color={labelFontWeight ? "black" : "inherit"}
                                sx={{
                                    flexGrow: 1,
                                    fontWeight: labelFontWeight ? labelFontWeight : 'inherit'
                    }}>
                        {labelText}
                    </Typography>
                    {buttons}
                    {/*<DocumentTreeItemEditButton onClickEdit/>*/}
                    {/*<DocumentTreeItemMenuButton*/}
                    {/*    onClickNewDocument={onClickNewDocument}*/}
                    {/*    onClickRename={onClickRename}*/}
                    {/*    onClickDelete={onClickDelete}*/}
                    {/*/>*/}
                </Box>
            }
            style={styleProps}
            {...other}
            ref={ref}
        />
    );
});

export default DocumentTreeItem;
