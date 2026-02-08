'use client'

import { useState, useRef } from 'react'
import Link from 'next/link'

export default function MeasurementPage() {
    const [gender, setGender] = useState('male')
    const [mode, setMode] = useState('upload')
    const [imagePreview, setImagePreview] = useState(null)
    const [measurements, setMeasurements] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [stream, setStream] = useState(null)

    const videoRef = useRef(null)
    const canvasRef = useRef(null)
    const fileInputRef = useRef(null)

    const startCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 }
            })
            if (videoRef.current) {
                videoRef.current.srcObject = mediaStream
                setStream(mediaStream)
            }
            setMode('camera')
            setError(null)
        } catch (err) {
            setError('Camera access denied. Please allow camera permissions.')
        }
    }

    const stopCamera = () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop())
            setStream(null)
        }
    }

    const capturePhoto = () => {
        if (videoRef.current && canvasRef.current) {
            const canvas = canvasRef.current
            const video = videoRef.current
            canvas.width = video.videoWidth
            canvas.height = video.videoHeight
            const ctx = canvas.getContext('2d')
            ctx.drawImage(video, 0, 0)

            canvas.toBlob((blob) => {
                const url = URL.createObjectURL(blob)
                setImagePreview(url)
                stopCamera()
                processImage(blob)
            }, 'image/jpeg')
        }
    }

    const handleFileUpload = (e) => {
        const file = e.target.files[0]
        if (file) {
            const url = URL.createObjectURL(file)
            setImagePreview(url)
            processImage(file)
        }
    }

    const processImage = async (imageBlob) => {
        setLoading(true)
        setError(null)
        setMeasurements(null)

        try {
            const reader = new FileReader()
            reader.readAsDataURL(imageBlob)
            reader.onloadend = async () => {
                const base64Image = reader.result.split(',')[1]

                const response = await fetch('http://localhost:5000/api/measure', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: base64Image, gender: gender })
                })

                if (!response.ok) {
                    throw new Error('AI server not responding. Make sure it is running on port 5000.')
                }

                const data = await response.json()
                setMeasurements(data)
                setLoading(false)
            }
        } catch (err) {
            setError(err.message)
            setLoading(false)
        }
    }

    const resetMeasurement = () => {
        setImagePreview(null)
        setMeasurements(null)
        setError(null)
        if (fileInputRef.current) fileInputRef.current.value = ''
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="bg-white rounded-2xl shadow-2xl p-8 mb-8">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-4xl font-bold text-purple-600 mb-2">📏 Body Measurement</h1>
                            <p className="text-gray-600">Capture or upload a full-body photo for AI-powered measurements</p>
                        </div>
                        <Link href="/" className="bg-gray-200 hover:bg-gray-300 px-6 py-3 rounded-lg font-semibold transition">
                            ← Back to Home
                        </Link>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Left: Capture/Upload */}
                    <div className="bg-white rounded-2xl shadow-xl p-6">
                        <h2 className="text-2xl font-semibold text-purple-600 mb-4">Step 1: Capture Image</h2>

                        {/* Gender Selection */}
                        <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Select Gender:</label>
                            <div className="flex gap-4">
                                <button
                                    onClick={() => setGender('male')}
                                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition ${gender === 'male' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                        }`}
                                >
                                    👨 Male
                                </button>
                                <button
                                    onClick={() => setGender('female')}
                                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition ${gender === 'female' ? 'bg-pink-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                        }`}
                                >
                                    👩 Female
                                </button>
                            </div>
                        </div>

                        {/* Mode Selection */}
                        <div className="flex gap-4 mb-4">
                            <button
                                onClick={() => { setMode('upload'); stopCamera(); }}
                                className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${mode === 'upload' ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                📤 Upload Image
                            </button>
                            <button
                                onClick={startCamera}
                                className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${mode === 'camera' ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                            >
                                📷 Use Camera
                            </button>
                        </div>

                        {/* Camera View */}
                        {mode === 'camera' && (
                            <div className="mb-4">
                                <video ref={videoRef} autoPlay playsInline className="w-full rounded-lg bg-black" />
                                <button
                                    onClick={capturePhoto}
                                    className="w-full mt-4 bg-green-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-green-700 transition"
                                >
                                    📸 Capture Photo
                                </button>
                            </div>
                        )}

                        {/* Upload View */}
                        {mode === 'upload' && (
                            <div className="mb-4">
                                <input
                                    ref={fileInputRef}
                                    type="file"
                                    accept="image/*"
                                    onChange={handleFileUpload}
                                    className="hidden"
                                />
                                <button
                                    onClick={() => fileInputRef.current?.click()}
                                    className="w-full bg-purple-600 text-white py-12 px-6 rounded-lg font-medium hover:bg-purple-700 transition border-2 border-dashed border-purple-300"
                                >
                                    <div className="text-4xl mb-2">📁</div>
                                    <div>Click to Upload Image</div>
                                    <div className="text-sm opacity-75 mt-1">JPG, PNG, or JPEG</div>
                                </button>
                            </div>
                        )}

                        {/* Image Preview */}
                        {imagePreview && (
                            <div className="mb-4">
                                <h3 className="font-semibold mb-2">Preview:</h3>
                                <img src={imagePreview} alt="Preview" className="w-full rounded-lg border-2 border-gray-300" />
                            </div>
                        )}

                        {/* Error Display */}
                        {error && (
                            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
                                <strong>Error:</strong> {error}
                            </div>
                        )}

                        {/* Loading */}
                        {loading && (
                            <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded-lg">
                                <div className="flex items-center">
                                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-700 mr-3"></div>
                                    Processing image with MediaPipe AI...
                                </div>
                            </div>
                        )}

                        <canvas ref={canvasRef} className="hidden" />
                    </div>

                    {/* Right: Results */}
                    <div className="bg-white rounded-2xl shadow-xl p-6">
                        <h2 className="text-2xl font-semibold text-purple-600 mb-4">Step 2: View Measurements</h2>

                        {!measurements && !loading && (
                            <div className="text-center text-gray-500 py-12">
                                <div className="text-6xl mb-4">📐</div>
                                <p>Measurements will appear here after processing</p>
                            </div>
                        )}

                        {measurements && (
                            <div className="space-y-4">
                                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mb-4">
                                    ✓ Measurements calculated successfully!
                                </div>

                                {/* Confidence Score */}
                                {measurements.confidence !== undefined && (
                                    <div className="bg-blue-50 p-4 rounded-lg">
                                        <div className="flex justify-between items-center">
                                            <span className="font-medium">Confidence Score:</span>
                                            <span className="text-2xl font-bold text-blue-600">
                                                {(measurements.confidence * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                    </div>
                                )}

                                {/* Measurements */}
                                <div className="space-y-3">
                                    <h3 className="font-semibold text-lg border-b pb-2">
                                        Body Measurements ({gender === 'male' ? 'Male' : 'Female'})
                                    </h3>

                                    {measurements.measurements && Object.entries(measurements.measurements).map(([key, value]) => (
                                        <div key={key} className="flex justify-between items-center py-2 border-b border-gray-200">
                                            <span className="capitalize font-medium text-gray-700">
                                                {key.replace(/_/g, ' ')}:
                                            </span>
                                            <span className="text-lg font-semibold text-purple-600">
                                                {typeof value === 'number' ? value.toFixed(1) : value} cm
                                            </span>
                                        </div>
                                    ))}
                                </div>

                                {/* Size Recommendation */}
                                {measurements.size_recommendation && (
                                    <div className="bg-purple-50 p-4 rounded-lg mt-4">
                                        <h3 className="font-semibold mb-2">Recommended Size:</h3>
                                        <div className="text-3xl font-bold text-purple-600">
                                            {measurements.size_recommendation}
                                        </div>
                                    </div>
                                )}

                                {/* Action Buttons */}
                                <div className="flex gap-3 mt-6">
                                    <button
                                        onClick={resetMeasurement}
                                        className="flex-1 bg-gray-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-gray-700 transition"
                                    >
                                        🔄 New Measurement
                                    </button>
                                    <button
                                        onClick={() => alert('Save functionality coming soon!')}
                                        className="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-green-700 transition"
                                    >
                                        💾 Save Results
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Instructions */}
                <div className="bg-white rounded-2xl shadow-xl p-6 mt-6">
                    <h3 className="text-xl font-semibold text-purple-600 mb-3">📋 Instructions for Best Results</h3>
                    <ul className="space-y-2 text-gray-700">
                        <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            Stand in a well-lit area with plain background
                        </li>
                        <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            Wear fitted clothing or minimal clothing
                        </li>
                        <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            Stand straight with arms slightly away from body
                        </li>
                        <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            Ensure full body is visible in the frame
                        </li>
                        <li className="flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            Face the camera directly (front view works best)
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    )
}
