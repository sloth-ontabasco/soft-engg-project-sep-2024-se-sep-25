export async function login(jwt) {
    const res = await fetch(import.meta.env.VITE_SERVER_BASE_URL + "/token", {
        method: "GET",
        headers: header(jwt),
    });

    if (res.status == 200) {
        return res.json();
    }

    throw new Error("Login Failed");
}

export function logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
}

export function header(jwt=null) {
    let token = jwt ? jwt : localStorage.getItem("token");
    if (token) {
        return { Authorization: "Bearer " + token };
    } else {
        return {};
    }
}

export async function getCurrentUser() {
    const res = await fetch(import.meta.env.VITE_SERVER_BASE_URL + "user", {
        method: "GET",
        headers: header(),
    });
    if (res.status == 200)
        return res.json();
    throw new Error('Failed fetching current user')
}