"use client"

import { useState } from "react"
import { endpoints } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Bug, Play } from "lucide-react"
import ReactMarkdown from "react-markdown"

export default function DebugPage() {
    const [logData, setLogData] = useState("")
    const [context, setContext] = useState("")
    const [analysis, setAnalysis] = useState("")
    const [loading, setLoading] = useState(false)

    const handleAnalyze = async () => {
        if (!logData.trim()) return

        setLoading(true)
        setAnalysis("")

        try {
            const res = await endpoints.rootCause(logData, context)
            setAnalysis(res.data.analysis)
        } catch (error) {
            setAnalysis("Error: Failed to analyze logs.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="flex min-h-screen flex-col items-center p-8 bg-slate-50">
            <div className="max-w-4xl w-full">
                <h1 className="text-3xl font-bold mb-8 flex items-center gap-2">
                    <Bug className="text-red-500" /> Log Debugger
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="space-y-4">
                        <Card>
                            <CardHeader>
                                <CardTitle>Input Logs</CardTitle>
                                <CardDescription>Paste the error log and any context below.</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div>
                                    <label className="text-sm font-medium mb-1 block">Error Log</label>
                                    <Textarea
                                        placeholder="Paste error log here..."
                                        className="h-32 font-mono text-xs"
                                        value={logData}
                                        onChange={(e) => setLogData(e.target.value)}
                                    />
                                </div>
                                <div>
                                    <label className="text-sm font-medium mb-1 block">Context (Optional)</label>
                                    <Input
                                        placeholder="Service name, timestamp, trace ID..."
                                        value={context}
                                        onChange={(e) => setContext(e.target.value)}
                                    />
                                </div>
                                <Button onClick={handleAnalyze} disabled={loading} className="w-full">
                                    {loading ? "Analyzing..." : "Analyze Root Cause"}
                                    {!loading && <Play size={16} className="ml-2" />}
                                </Button>
                            </CardContent>
                        </Card>
                    </div>

                    <div className="h-full">
                        <Card className="h-full min-h-[400px]">
                            <CardHeader>
                                <CardTitle>AI Analysis</CardTitle>
                            </CardHeader>
                            <CardContent>
                                {loading ? (
                                    <div className="flex items-center justify-center h-40 text-slate-400 animate-pulse">
                                        Analyzing log patterns...
                                    </div>
                                ) : analysis ? (
                                    <div className="prose prose-sm max-w-none dark:prose-invert">
                                        <ReactMarkdown>{analysis}</ReactMarkdown>
                                    </div>
                                ) : (
                                    <div className="flex items-center justify-center h-40 text-slate-400 text-sm italic">
                                        Analysis results will appear here.
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </main>
    )
}
