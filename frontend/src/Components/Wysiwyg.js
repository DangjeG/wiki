import {convertToHTML} from 'draft-convert';
import React, { useState, useEffect } from 'react';
import {EditorState, ContentState, convertFromHTML} from 'draft-js';
import {Editor}  from 'react-draft-wysiwyg';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';
import {toolbar} from "../Configs/wysiwyg.toolbar.config";

export default function Wysiwyg(props){

    const handleChange = (html) => {
        props.onChange(html)
    }

    const [editorState, setEditorState] = React.useState(
        () => EditorState.createWithContent(
            ContentState.createFromBlockArray(
                convertFromHTML(props.content)
        )
    ))

    useEffect(() => {
        let html = convertToHTML(editorState.getCurrentContent());
        handleChange(html)
    }, [editorState]);


    return (
        <>
            <Editor
                toolbar={toolbar}
                editorState={editorState}
                onEditorStateChange={setEditorState}/>
        </>
    )
}
