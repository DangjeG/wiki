import {Editor} from 'react-draft-wysiwyg';
import { convertToHTML } from 'draft-convert';
import React, { useState, useEffect } from 'react';
import { EditorState } from 'draft-js';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';


export default function Wysiwyg({onChange}){

    const handleChange = () => {
        onChange(convertedContent)
    }

    const [editorState, setEditorState] = useState(() => EditorState.createEmpty());
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
                onEditorStateChange={setEditorState}

            />
        </>
    )
}
