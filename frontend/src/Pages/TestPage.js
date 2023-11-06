import Wysiwyg from "../Components/Wysiwyg";
import {useState} from "react";
import BlockComponent from "../Components/Block";


export default function TestPage(){

    const [blockData, setBlockData] = useState("<h1> Hello </h1> ");

    return (
        <>
            <BlockComponent content={blockData}/>
            <Wysiwyg onChange={(data) => {
                setBlockData(data)
            }}/>
        </>

    )

}