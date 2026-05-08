"use client";
import React, { SubmitEvent, useState } from 'react'
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import api from '@/app/api/Api';
import { ACCESS_TOKEN, REFRESH_TOKEN } from './constant';
import { BarLoader } from 'react-spinners';

type Props = {
    method: string;
    route: string;
}

const Form = ({ method, route }: Props) => {
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const router = useRouter();

    const handleSubmit = async (e: SubmitEvent<HTMLElement>) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await api.post(route, {
                username, 
                password
            });
            if (method === "login") {
                toast.success("Login successful!");
                cookieStore.set(ACCESS_TOKEN, response.data.access);
                cookieStore.set(REFRESH_TOKEN, response.data.refresh);
                router.replace("/home");
            } else {
                toast.success("Registration successful! Please login.");
                router.replace("/");
            }
        } catch (error) {
            toast.error("An error occurred. Please try again.");
        } finally {
            setLoading(false);
        }
    }
    return (
        <form onSubmit={handleSubmit}>
            <fieldset className="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
                <legend className="fieldset-legend">{method === "login" ? "Login" : "Register"}</legend>

                <label className="label">Username</label>
                <input
                    type="text"
                    className="input"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />

                <label className="label">Password</label>
                <input
                    type="password"
                    className="input"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                <button className="btn btn-neutral mt-4" type='submit' disabled={loading}>{method === "login" ? "Login" : "Register"}</button>
                {loading && (
                    <div className='w-full flex justify-center'>
                        <BarLoader 
                        color='#e58d47'
                        />
                    </div>
                    
                )}
            </fieldset>
        </form>
    )
}

export default Form
