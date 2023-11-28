import React from "react";
import BlockComponent from "../Components/Block";


export default function TestPage(){

    const blocks =
        [
            {
                id: "321",
                content: "<p>Hello1</p>"
            },
            {
                id: "123",
                content: "<p>Hello2</p>"
            }
        ]

    return (
        <>
            {blocks.map((item) => {
                return <BlockComponent block={item} onCange={()=>{}}/>
            })}

        </>
    )

}