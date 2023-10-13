


export default function Home(){


    function onc() {
       localStorage.setItem("token", "234")
       /*api.emit("isLogin", true)*/
   }
     async function onc2() {
         localStorage.setItem("token", "")
         /*await api.logout()*/
     }

    return(
        <div>
            <form >
                <button onClick={onc}>
                    login
                </button>
                <button onClick={onc2}>
                    logout
                </button>
            </form>
        </div>
    )
}