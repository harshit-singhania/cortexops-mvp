"use client"

import { useState } from "react"
import { endpoints } from "@/lib/api"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Send, Bot, User } from "lucide-react"

interface Message {
    role: "user" | "assistant"
    content: string
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)

    const handleSend = async () => {
        if (!input.trim()) return

        const userMsg: Message = { role: "user", content: input }
        setMessages(prev => [...prev, userMsg])
        setInput("")
        setLoading(true)

        try {
            const res = await endpoints.chat(input)
            const botMsg: Message = { role: "assistant", content: res.data.response }
            setMessages(prev => [...prev, botMsg])
        } catch (error) {
            const errorMsg: Message = { role: "assistant", content: "Error: Failed to get response." }
            setMessages(prev => [...prev, errorMsg])
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="flex min-h-screen flex-col items-center p-8 bg-slate-50">
            <div className="max-w-4xl w-full">
                <h1 className="text-3xl font-bold mb-8">System Chat</h1>

                <Card className="h-[600px] flex flex-col">
                    <CardHeader className="border-b">
                        <CardTitle>Conversation</CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 p-0 overflow-hidden flex flex-col">
                        <ScrollArea className="flex-1 p-4">
                            <div className="space-y-4">
                                {messages.map((msg, i) => (
                                    <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                                        <div className={`flex gap-2 max-w-[80%] ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                                            <div className={`p-2 rounded-full h-8 w-8 flex items-center justify-center ${msg.role === "user" ? "bg-blue-100" : "bg-slate-100"}`}>
                                                {msg.role === "user" ? <User size={16} /> : <Bot size={16} />}
                                            </div>
                                            <div className={`p-3 rounded-lg text-sm ${msg.role === "user" ? "bg-blue-500 text-white" : "bg-slate-100 text-slate-800"}`}>
                                                {msg.content}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                                {loading && (
                                    <div className="flex justify-start">
                                        <div className="bg-slate-100 p-3 rounded-lg text-sm animate-pulse">Thinking...</div>
                                    </div>
                                )}
                            </div>
                        </ScrollArea>

                        <div className="p-4 border-t flex gap-2">
                            <Input
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                                placeholder="Ask about your system..."
                            />
                            <Button onClick={handleSend} disabled={loading}>
                                <Send size={16} />
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </main>
    )
}
