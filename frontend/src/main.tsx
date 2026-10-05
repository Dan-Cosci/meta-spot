import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { Toaster } from 'react-hot-toast';
import { RouterProvider } from 'react-router/dom';
import { ThemeProvider } from './hooks/Theme.tsx';
import { DownloadProvider } from './hooks/Download.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <DownloadProvider>
      <ThemeProvider>
        <RouterProvider router={App} />
      </ThemeProvider>
      <Toaster
        position='top-center'
        reverseOrder={ false }
      />
    </DownloadProvider>

  </StrictMode>,
)
