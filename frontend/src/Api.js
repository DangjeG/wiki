import {instance} from "./api.config";
import type {User} from "./Models/User";

export default class Api {
    isLogin() {
        return (!(localStorage.getItem("token").length === 0))
    }

    async login(path, email) {
        await instance.post(`/auth/login`,
            {
                "email": email
            }).then((response) => {
            localStorage.setItem('verify', response.data.verify_token)
        })
    }

    async signup(email, username, first_name, last_name, second_name, is_user_agreement_accepted) {
        await instance.post(`/auth/signup`,
            {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "second_name": second_name,
                "is_user_agreement_accepted": is_user_agreement_accepted,
                "organization_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }).then((response) => {
            localStorage.setItem('verify', response.data.verify_token)
        })
    }

    async verify(code) {
        await instance.get(`/auth/verify`,`token=${localStorage.getItem("verify")}&verification_code=${code}`)
            .then((resp) => {
                localStorage.setItem("token", resp.data.msg);
            })
    }

    async logout() {
        localStorage.setItem('token', "");
    }

    async getUsers() : User[]{
        let users = []
        await instance.get(`/user/all`,)
            .then((resp) => {
                resp.data.forEach((user)=>{
                        users.push(new User(user.email, user.username, user.first_name, user.last_name, user.second_name, user.responsibility))
                    }
                )
            })
        return users
    }
}