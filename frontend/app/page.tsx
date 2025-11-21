import Link from "next/link"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { MessageSquare, Bug, FileText, Activity } from "lucide-react"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24 bg-slate-50">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex mb-12">
        <h1 className="text-4xl font-bold text-slate-900 tracking-tight">CortexOps</h1>
        <p className="text-slate-500">System Intelligence & Observability</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">
        <Link href="/chat" className="hover:scale-105 transition-transform">
          <Card className="h-full border-slate-200 shadow-sm hover:shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5 text-blue-500" />
                System Chat
              </CardTitle>
              <CardDescription>Ask questions about your system architecture and status.</CardDescription>
            </CardHeader>
          </Card>
        </Link>

        <Link href="/debug" className="hover:scale-105 transition-transform">
          <Card className="h-full border-slate-200 shadow-sm hover:shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bug className="h-5 w-5 text-red-500" />
                Log Debugger
              </CardTitle>
              <CardDescription>Analyze error logs and find root causes with AI.</CardDescription>
            </CardHeader>
          </Card>
        </Link>

        <Link href="/docs" className="hover:scale-105 transition-transform">
          <Card className="h-full border-slate-200 shadow-sm hover:shadow-md">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-green-500" />
                Auto-Docs
              </CardTitle>
              <CardDescription>Generate and view documentation for your services.</CardDescription>
            </CardHeader>
          </Card>
        </Link>
      </div>

      <div className="mt-12 w-full max-w-5xl">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-purple-500" />
              System Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-green-500"></div>
                <span>Backend API: Online</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-green-500"></div>
                <span>Vector DB: Online</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-green-500"></div>
                <span>Redis Cache: Online</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
