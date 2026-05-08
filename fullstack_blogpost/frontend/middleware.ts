
import { NextResponse } from "next/server"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./utils/constant"
import { jwtDecode } from "jwt-decode"
import { cookies } from "next/headers";
import api from "./app/api/Api";

export default async function middleware(request: Request) {

    const cookieStorage = await cookies();

    const refreshToken = async () => {
        const refreshToken = cookieStorage.get(REFRESH_TOKEN);
        try {
            const response = await api.post("api/token/refresh/", {
                refresh: refreshToken
            });
            if (response.status === 200) {
                const { access } = response.data;
                cookieStorage.set(ACCESS_TOKEN, access)
    
            }
            else {
                return NextResponse.redirect(new URL("/", request.url));
            }
        } catch (error) {
            console.error(error);
            return NextResponse.redirect(new URL("/", request.url));

        }
    }

    const auth = async () => {
        const accessToken = cookieStorage.get(ACCESS_TOKEN);
        if (!accessToken) {

            return NextResponse.redirect(new URL("/", request.url));
        }
        try {
            const decodedToken: any = jwtDecode(accessToken.value);
            const expiredAt = decodedToken.exp;
            const currentTime = Date.now() / 1000;
            if (expiredAt < currentTime) {

                refreshToken();
            }
        } catch (e) {

            return NextResponse.redirect(new URL("/", request.url));
        }
    }

    auth();



    return NextResponse.next();
}

export const config = {
    matcher: ["/home"]
}