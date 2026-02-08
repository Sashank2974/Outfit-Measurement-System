'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

export default function Home() {
    const [backendStatus, setBackendStatus] = useState('checking')
    const [aiStatus, setAiStatus] = useState('checking')

    useEffect(() => {
        checkServices()
    }, [])

    const checkServices = async () => {
        // Check backend
        try {
            const res = await fetch('http://localhost:8000/health')
            setBackendStatus(res.ok ? 'online' : 'offline')
        } catch {
            setBackendStatus('offline')
        }

        // Check AI server
        try {
            const res = await fetch('http://localhost:5000/health')
            setAiStatus(res.ok ? 'online' : 'offline')
        } catch {
            setAiStatus('offline')
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 p-8">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8">
                    <h1 className="text-4xl font-bold text-purple-600 mb-4">
                        🎯 AI Body Measurement System
                    </h1>
                    <p className="text-gray-600 text-lg">
                        Gender-Specific Body Measurement with Real AI Pose Detection
                    </p>
                </div>

                {/* Status */}
                <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
                    <h2 className="text-2xl font-semibold mb-4">System Status</h2>
                    <div className="space-y-2">
                        <div className="flex items-center gap-3">
                            <div className={`w-3 h-3 rounded-full ${backendStatus === 'online' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                            <span>Backend API: {backendStatus === 'online' ? 'Online ✓' : 'Offline ✗'}</span>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className={`w-3 h-3 rounded-full ${aiStatus === 'online' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                            <span>AI Server (MediaPipe): {aiStatus === 'online' ? 'Online ✓' : 'Offline ✗'}</span>
                        </div>
                    </div>
                </div>

                {/* Main Action */}
                <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
                    <h2 className="text-3xl font-bold text-purple-600 mb-6">
                        Get Your Body Measurements
                    </h2>
                    <p className="text-gray-600 mb-8 text-lg">
                        Use AI-powered pose detection to get accurate body measurements
                    </p>
                    <Link
                        href="/measurement"
                        className="inline-block bg-gradient-to-r from-purple-600 to-blue-600 text-white px-12 py-4 rounded-xl text-xl font-semibold hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-lg"
                    >
                        📏 Start Measurement
                    </Link>
                </div>

                {/* Features */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <div className="text-4xl mb-3">📷</div>
                        <h3 className="font-bold text-lg mb-2">Camera or Upload</h3>
                        <p className="text-gray-600 text-sm">Capture with webcam or upload existing photos</p>
                    </div>
                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <div className="text-4xl mb-3">🤖</div>
                        <h3 className="font-bold text-lg mb-2">AI Pose Detection</h3>
                        <p className="text-gray-600 text-sm">MediaPipe 0.10.32 for accurate measurements</p>
                    </div>
                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <div className="text-4xl mb-3">👕</div>
                        <h3 className="font-bold text-lg mb-2">Size Recommendations</h3>
                        <p className="text-gray-600 text-sm">Get clothing size suggestions based on measurements</p>
                    </div>
                </div>

                {/* Footer */}
                <div className="text-center text-white mt-8 p-6">
                    <p className="text-lg font-semibold">AI-Based Body Size Measurement System v1.0.0</p>
                    <p className="text-sm opacity-90">Backend: FastAPI | Frontend: Next.js + React | AI: MediaPipe 0.10.32</p>
                </div>
            </div>
        </div>
    )
}
