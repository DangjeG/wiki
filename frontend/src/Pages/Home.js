import {instance} from "../api.config";


export default function Home(){


    async function onc(event) {
        event.preventDefault();
        await instance.get(`/user/all`)
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