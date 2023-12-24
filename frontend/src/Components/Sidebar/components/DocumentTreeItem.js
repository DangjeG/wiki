import React, {useState} from "react";
import {useTheme} from "@mui/material/styles";
import {Box, Typography} from "@mui/material";
import DocumentTreeItemRoot from "./DocumentTreeItemRoot";
import "../../../Styles/Sidebar.css"


const DocumentTreeItem = React.forwardRef(function StyledTreeItem(props, ref) {

    const [showMenu, setShowMenu] = useState(false);

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
        buttons,
        ...other
    } = props;

    const styleProps = {
        '--tree-view-color': theme.palette.mode !== 'dark' ? color : colorForDarkMode,
        '--tree-view-bg-color':
            theme.palette.mode !== 'dark' ? bgColor : bgColorForDarkMode,
    };

    const handleMouseEnter = () => {
        setShowMenu(true);
    };

    const handleMouseLeave = () => {
        setShowMenu(false);
    };

    return (
        <DocumentTreeItemRoot
            label={
                <Box
                    onMouseEnter={handleMouseEnter}
                    onMouseLeave={handleMouseLeave}
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                        p: 0.5,
                        pr: 0,
                        minHeight: "48px"
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
                    <div className={showMenu? "item-toolbar_visibility_visible" : "item-toolbar_visibility_hidden"}>
                        {buttons}
                    </div>
                </Box>
            }
            style={styleProps}
            {...other}
            ref={ref}
        />
    );
});

export default DocumentTreeItem;
