import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { Toaster } from 'react-hot-toast';
import { RouterProvider } from 'react-router/dom';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={App} />
    <Toaster
      position='top-center'
      reverseOrder={ false }
    />
  </StrictMode>,
)
