"use client";


import { useEffect } from "react";
import { useRouter } from "next/navigation";


const LogoutPage = () => {
  const router = useRouter();
  useEffect(() => {
    // Supprime les cookies côté client
    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    // Redirige vers la page d'accueil
    router.replace("/");
  }, [router]);
  return (
    <div>
      <h1>Déconnexion...</h1>
    </div>
  );
}

export default LogoutPage
