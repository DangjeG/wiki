



export default function FileUploader({onChange}){

    const handleChange = (e) => {
        onChange(e)
    }

    return(<input type="file" onChange={handleChange}/>)
}