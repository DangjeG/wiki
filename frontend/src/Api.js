import {instance} from "./api.config";
import {User} from "./Models/User";
import {Organization} from "./Models/Organization";

export default class Api {


    isLogin() {
        return (!(localStorage.getItem("token").length === 0))
    }


    async login(email) {
        await instance.post(`/auth/login`,
            {
                "email": email
            }).then((response) => {
            localStorage.setItem('verify', response.data.verify_token)
        })
    }


    async signup(email, username, first_name, last_name, second_name,  organization_id, is_user_agreement_accepted) {
        await instance.post(`/auth/signup`,
            {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "second_name": second_name,
                "is_user_agreement_accepted": is_user_agreement_accepted,
                "organization_id": organization_id
            }).then((response) => {
            localStorage.setItem('verify', response.data.verify_token)
        })
    }


    async verify(code) {
        await instance.get(`/auth/verify?token=${localStorage.getItem("verify")}&verification_code=${code}`)
            .then((resp) => {
                localStorage.setItem("token", resp.data.msg);
            })
    }

    async logout() {
        localStorage.setItem('token', "");
    }


     async getUsers() {
         let users = []
         await instance.get(`/user/all`,)
             .then((resp) => {
                 resp.data.forEach((user) => {
                     if (user.wiki_api_client === null) {
                         users.push(new User(user.email, user.username, user.first_name, user.last_name, user.second_name, ""))
                     }
                     else {
                         users.push(new User(user.email, user.username, user.first_name, user.last_name, user.second_name, user.wiki_api_client.responsibility))
                     }
                 })
             })
         return users;
     }


     async getOrganizations() {
         let organizations = []
         await instance.get(`/organization/all`,)
             .then((resp) => {
                 resp.data.forEach((organization) => {
                         organizations.push(new Organization(organization.access, organization.description, organization.id, organization.name))
                     }
                 )
             })
         return organizations
     }

    async addOrganizations(name, description, access){
        await instance.post(`/organization/`,
            {
                "name": name,
                "description": description,
                "access": access
            })
    }

    async getMe() {
        let user
        await instance.get(`/user/me`,)
            .then((resp) => {
                user = new User(resp.data.email, resp.data.username, resp.data.first_name, resp.data.last_name, resp.data.second_name, resp.data.wiki_api_client.responsibility)
            })

        return user
    }
}