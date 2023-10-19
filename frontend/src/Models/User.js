

export class User{
    email;
    username;
    first_name;
    last_name;
    second_name;
    responsibility;
    constructor(email, username, first_name, last_name, second_name, responsibility) {
        this.email = email;
        this.username = username;
        this.first_name = first_name;
        this.last_name = last_name;
        this.second_name = second_name;
        this.responsibility = responsibility;
    }

}