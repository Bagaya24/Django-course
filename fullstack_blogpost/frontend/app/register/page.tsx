"use client"
import Form from '@/utils/Form'
import React from 'react'
import toast from 'react-hot-toast'

export default function RegisterPage() {
    
  return (
    <div className='w-full h-screen flex justify-center items-center'>
      <Form method="register" route="/users/register/" />
    </div>
  )
}
