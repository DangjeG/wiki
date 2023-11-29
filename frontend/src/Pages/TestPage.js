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
           <img src={"https://4.downloader.disk.yandex.ru/preview/071c52a6812838258ca8c1cd0ca50858e7f497b6af958745739abd6f2e70d55e/inf/P1Uu3IBvn2J_059WhlC9XydbkJ2sC_KEk2e_VtbYAOfuuRRO_ACnqYduWLfxvvz5VgHzs7xBXDvk4Qqe7B86gQ%3D%3D?uid=1852241993&filename=%D0%93%D0%BE%D1%80%D1%8B.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=1852241993&tknv=v2&size=1864x939"}/>
        </>
    )

}