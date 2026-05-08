import Form from '@/utils/Form'
import React from 'react'

export default function LoginPage() {
  return (
    <div className='w-full h-screen flex justify-center items-center'>
      <Form method="login" route="/users/token/" />
    </div>
  )
}
