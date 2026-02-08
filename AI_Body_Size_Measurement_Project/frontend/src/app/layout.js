import './globals.css'

export const metadata = {
    title: 'AI Body Measurement System',
    description: 'AI-powered body measurement with MediaPipe',
}

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    )
}
