import {api} from "../../../../Config/app.config";


export default function FileUploader({block, onChange}){

    const handleChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            let formData = new FormData();
            formData.append('file', file);
            api.updateFileBlockData(block.id, formData).then((newBlock) => {
                onChange(newBlock)
            });
        }
    }

    return(<input type="file" onChange={handleChange}/>)
}