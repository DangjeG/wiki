import axios from "axios";

export const instance = axios.create({
    withCredentials: true,
    baseURL: `https://2fdc-176-59-193-145.ngrok-free.app/api/v1`,
});
instance.interceptors.request.use(
    (config) => {
        let token = localStorage.getItem("token")
        if(token)
            config.headers.Authorization = `Bearer ${token}`
        return config
    }
)


//todo сделать когда будет рефреш токен
/*
instance.interceptors.response.use(
    // в случае валидного accessToken ничего не делаем:
    (config) => {
        return config;
    },
    // в случае просроченного accessToken пытаемся его обновить:
    async (error) => {
        // предотвращаем зацикленный запрос, добавляя свойство _isRetry
        const originalRequest = {...error.config};
        originalRequest._isRetry = true;
        if (
            // проверим, что ошибка именно из-за невалидного accessToken
            error.response.status === 401 &&
            // проверим, что запрос не повторный
            error.config &&
            !error.config._isRetry
        ) {
            try {
                // запрос на обновление токенов
                const resp = await instance.get("/auth/refresh");
                // сохраняем новый accessToken в localStorage
                localStorage.setItem("token", resp.data.access_token);
                // переотправляем запрос с обновленным accessToken
                return instance.request(originalRequest);
            } catch (error) {
                console.log("AUTH ERROR");
            }
        }
        // на случай, если возникла другая ошибка (не связанная с авторизацией)
        // пробросим эту ошибку
        throw error;
    }
);*/
