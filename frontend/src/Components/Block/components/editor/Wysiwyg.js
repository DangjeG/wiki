import {convertToHTML} from 'draft-convert';
import React, { useState, useEffect } from 'react';
import {EditorState, ContentState, convertFromHTML} from 'draft-js';
import {Editor}  from 'react-draft-wysiwyg';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';
import {toolbar} from "../../../../Config/wysiwyg.toolbar.config";

export default function Wysiwyg({block, onChange}){


    const handleChange = (newBlock) => {
        onChange(newBlock)
    }

    const [editorState, setEditorState] = React.useState(
        () => EditorState.createWithContent(
            ContentState.createFromBlockArray(
                convertFromHTML(block.content)
        )
    ))

    useEffect(() => {
        let html = convertToHTML(editorState.getCurrentContent());
        block.content = html
        handleChange(block)
    }, [editorState]);


    return (
        <div>
            <Editor
                toolbar={toolbar}
                editorState={editorState}
                onEditorStateChange={setEditorState}/>
        </div>
    )
}
