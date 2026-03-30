'use client';

import { useState, useEffect } from 'react';
import { fetchEmails, simulateEmail, EmailRecord } from '@/lib/api';
import EmailCard from '@/components/EmailCard';

export default function GmailDashboard() {
  const [emails, setEmails] = useState<EmailRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [isSimulating, setIsSimulating] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await fetchEmails();
      // Sort by newest first
      setEmails(data.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulate = async () => {
    setIsSimulating(true);
    try {
      await simulateEmail();
      await loadData();
    } catch (err) {
      alert("Simulation failed. Check if Backend is running on Port 8000");
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="flex h-screen bg-white text-gray-900 font-sans">
      {/* 1. Left Sidebar (The Gmail Look) */}
      <aside className="w-64 border-r border-gray-200 flex flex-col p-4 bg-gray-50/50">
        <div className="flex items-center gap-2 mb-8 px-2">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold">S</div>
          <span className="text-xl font-bold tracking-tight">Sinneo AI</span>
        </div>

        <button
          onClick={handleSimulate}
          disabled={isSimulating}
          className="w-full py-4 mb-6 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 rounded-2xl font-semibold transition-all flex items-center justify-center gap-2 shadow-sm border border-indigo-200 disabled:opacity-50"
        >
          {isSimulating ? "Processing..." : "＋ Simulate Email"}
        </button>

        <nav className="space-y-1">
          <div className="px-4 py-2 bg-indigo-50 text-indigo-700 rounded-lg font-medium flex justify-between items-center">
            <span>All Emails</span>
            <span className="text-xs">{emails.length}</span>
          </div>
          <div className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg cursor-not-allowed">Sales</div>
          <div className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg cursor-not-allowed">Finance</div>
          <div className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg cursor-not-allowed">Calendar</div>
        </nav>
      </aside>

      {/* 2. Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header Bar */}
        <header className="h-16 border-b border-gray-200 flex items-center justify-between px-8 bg-white">
          <div className="flex items-center gap-4 w-full max-w-2xl">
            <input
              type="text"
              placeholder="Search processed emails..."
              className="w-full bg-gray-100 border-none rounded-full px-6 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
            />
          </div>
          <div className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-gray-200 border border-gray-300"></div>
          </div>
        </header>

        {/* Email List Wrapper */}
        <section className="flex-1 overflow-y-auto bg-gray-50/30">
          {loading ? (
            <div className="flex items-center justify-center h-full text-gray-400 animate-pulse font-medium">
              Synchronizing with AI Backend...
            </div>
          ) : emails.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <p className="text-lg">Your inbox is empty</p>
              <p className="text-sm">Click 'Simulate' to start the AI pipeline.</p>
            </div>
          ) : (
            <div className="max-w-5xl mx-auto py-6 px-4 space-y-4">
              {/* We use the EmailCard here. Since it's Gmail-style, 
                    it will look like a vertical stack of clean cards. */}
              {emails.map((email) => (
                <EmailCard key={email.id} record={email} />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}