"use client"

import { useState } from "react"
import { endpoints } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { FileText, Sparkles } from "lucide-react"
import ReactMarkdown from "react-markdown"

export default function DocsPage() {
    const [serviceName, setServiceName] = useState("")
    const [description, setDescription] = useState("")
    const [docs, setDocs] = useState("")
    const [loading, setLoading] = useState(false)

    const handleGenerate = async () => {
        if (!serviceName.trim()) return

        setLoading(true)
        setDocs("")

        try {
            const res = await endpoints.generateDocs(serviceName, description, {})
            setDocs(res.data.documentation)
        } catch (error) {
            setDocs("Error: Failed to generate documentation.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="flex min-h-screen flex-col items-center p-8 bg-slate-50">
            <div className="max-w-4xl w-full">
                <h1 className="text-3xl font-bold mb-8 flex items-center gap-2">
                    <FileText className="text-green-500" /> Auto-Docs
                </h1>

                <div className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Service Details</CardTitle>
                            <CardDescription>Enter service information to generate architecture docs.</CardDescription>
                        </CardHeader>
                        <CardContent className="flex gap-4 items-end">
                            <div className="flex-1 space-y-2">
                                <label className="text-sm font-medium">Service Name</label>
                                <Input
                                    placeholder="e.g., payment-service"
                                    value={serviceName}
                                    onChange={(e) => setServiceName(e.target.value)}
                                />
                            </div>
                            <div className="flex-[2] space-y-2">
                                <label className="text-sm font-medium">Description</label>
                                <Input
                                    placeholder="Brief description of what it does..."
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                />
                            </div>
                            <Button onClick={handleGenerate} disabled={loading}>
                                {loading ? "Generating..." : "Generate"}
                                {!loading && <Sparkles size={16} className="ml-2" />}
                            </Button>
                        </CardContent>
                    </Card>

                    {docs && (
                        <Card>
                            <CardHeader>
                                <CardTitle>Generated Documentation</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="prose prose-slate max-w-none p-4 bg-slate-50 rounded-lg border">
                                    <ReactMarkdown>{docs}</ReactMarkdown>
                                </div>
                            </CardContent>
                        </Card>
                    )}
                </div>
            </div>
        </main>
    )
}
