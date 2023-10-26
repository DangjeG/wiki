import {instance} from "./api.config";

export default class Api {
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
                         users.push(user)
                     }
                 )
             })
         return users;
    }


     async getOrganizations() {
         let organizations = []
         await instance.get(`/organization/all`,)
             .then((resp) => {
                 resp.data.forEach((organization) => {
                         organizations.push(organization)
                 })
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
        let user = null
          await instance.get(`/user/me`).then((resp) => {
              user = resp.data
         })
        return user
    }

    async approveUser(username, responsibility, description){
        await instance.post(`/admins/approve_user?username=${username}`, {
            "responsibility": responsibility,
            "api_client_description": description
        } )
    }

    async getWorkspaces(){
        let workspaces = []
        await instance.get(`/workspace/all`).then((resp)=>{
            resp.data.forEach((workspace) => {
                workspaces.push(workspace)
            })}
        )
       return workspaces
    }

    async addWorkspaces(title){
        await instance.post(`/workspace`,{
            "title" : title
        })
    }

    async getWorkspace(id){
        let workspace = null
        await instance.get(`/workspace/all`).then((resp)=>{
            workspace=resp.data
           }
        )
        return workspace
    }

    async addDocument(title, workspace_id, parent_document_id){
        await instance.post(`/document`,{
            "title" : title,
            "workspace_id": workspace_id,
            "parent_document_id": parent_document_id
        })
    }

    async getDocumentsTree(workspace_id){
        let documents = []
        await instance.get(`/document/tree?workspace_id=${workspace_id}`).then((resp)=>{
            resp.data.forEach((document) => {
                documents.push(document)
            })}
        )
        return documents
    }

    async addBlock(document_id, position, type_block){
        await instance.post(`/block`,{
            "document_id": document_id,
            "position": position,
            "type_block": type_block
        })
    }

    async deleteBlock(block_id){
        await instance.delete(`/block?block_id=${block_id}`)
    }

    async updateBlockData(block_id, content){
        await instance.put(`/block/data`,{
            "block_id": block_id,
            "content": content
        })
    }

    async getBlocks(document_id){
        let res = []
        await instance.get(`/block/data?document_id=${document_id}`).then((resp)=>{
            resp.data.forEach((item) => {
                res.push(item)
            })}
        )
        return res
    }
}