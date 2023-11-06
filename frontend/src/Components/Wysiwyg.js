import { convertToHTML } from 'draft-convert';
import React, { useState, useEffect } from 'react';
import {Editor, EditorState } from 'draft-js';
import 'draft-js/dist/Draft.css';

export default function Wysiwyg(props){

    const handleChange = () => {
        props.onChange(convertedContent)
    }

    const [editorState, setEditorState] = React.useState(
        () => EditorState.createEmpty(),
    ) ;
    const [convertedContent, setConvertedContent] = useState();

    useEffect(() => {
        let html = convertToHTML(editorState.getCurrentContent());
        setConvertedContent(html);
        handleChange(html)
    }, [editorState]);


    return (
        <>
            <Editor
                editorState={editorState}
                onChange={(data) =>{setEditorState(data)}}/>
        </>
    )
}
