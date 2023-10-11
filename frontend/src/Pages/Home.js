import {instance} from "../api.config";


export default function Home(){

    async function onc(event) {


        event.preventDefault();
        try {
             await instance.post(`/auth/test`).then( resp =>{
                 alert(resp.data)
             })
        } catch (error) {
            console.error(error);
        }
    }

    return(
        <div>
            <form onSubmit={onc}>
                <button type={"submit"}>
                    ryjgrf
                </button>
            </form>
        </div>
    )
}