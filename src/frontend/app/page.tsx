/**
 * app/page.tsx — The Dashboard Page
 *
 * This is your main (and only) page. In Next.js App Router,
 * every file named page.tsx inside the app/ folder becomes a route.
 * app/page.tsx → yoursite.com/
 *
 * Architecture decision: "use client"
 * ---------------------------------------------------------------
 * By default, Next.js App Router components are SERVER components.
 * Server components can't use React hooks (useState, useEffect)
 * or browser APIs (window, localStorage).
 *
 * We add "use client" because:
 * - We use useState to track the email list and loading state
 * - We use useEffect to fetch emails on mount
 * - We handle button click events
 *
 * A cleaner production pattern: use a Server Component to fetch
 * the initial data and a Client Component just for the "Simulate" button.
 * But for clarity, we keep everything here.
 */

"use client";

import { useEffect, useState } from "react";
import { EmailRecord, fetchEmails, simulateEmail } from "@/lib/api";
import EmailCard from "@/components/EmailCard";

export default function DashboardPage() {
  // ── State ──────────────────────────────────────────────────────
  const [emails, setEmails] = useState<EmailRecord[]>([]);
  const [loading, setLoading] = useState(true);       // Initial page load
  const [simulating, setSimulating] = useState(false); // Simulate button
  const [error, setError] = useState<string | null>(null);
  const [lastProcessed, setLastProcessed] = useState<string | null>(null);

  // ── Fetch emails on mount ──────────────────────────────────────
  // useEffect with [] runs once when the component first renders.
  // This is equivalent to componentDidMount in class components.
  useEffect(() => {
    loadEmails();
  }, []);

  async function loadEmails() {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchEmails();
      setEmails(data);
    } catch (err) {
      setError("Could not connect to backend. Is it running on port 8000?");
    } finally {
      setLoading(false);
    }
  }

  // ── Simulate a new email ───────────────────────────────────────
  async function handleSimulate() {
    try {
      setSimulating(true);
      setError(null);
      const newRecord = await simulateEmail();

      // Prepend new record to the top of the list (newest first)
      // Without re-fetching the entire list — more efficient
      setEmails((prev) => [newRecord, ...prev]);
      setLastProcessed(newRecord.intent.replace(/_/g, " "));
    } catch (err) {
      setError("Failed to simulate email. Check that the backend is running.");
    } finally {
      setSimulating(false);
    }
  }

  // ── Stats derived from current email list ─────────────────────
  // These recalculate automatically whenever `emails` changes
  const stats = {
    total: emails.length,
    sales: emails.filter((e) => e.department === "sales").length,
    calendar: emails.filter((e) => e.department === "calendar").length,
    finance: emails.filter((e) => e.department === "finance").length,
  };

  // ── Render ─────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gray-50">

      {/* ── Header ── */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              🤖 AI Operations Assistant
            </h1>
            <p className="text-sm text-gray-500">
              Automated email processing pipeline
            </p>
          </div>
          <div className="flex items-center gap-3">
            {/* Refresh button */}
            <button
              onClick={loadEmails}
              disabled={loading}
              className="text-sm text-gray-500 hover:text-gray-700 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              {loading ? "Loading..." : "↻ Refresh"}
            </button>

            {/* Simulate button — the main action */}
            <button
              onClick={handleSimulate}
              disabled={simulating}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
            >
              {simulating ? (
                <>
                  <span className="animate-spin inline-block">⟳</span>
                  Processing...
                </>
              ) : (
                "⚡ Simulate Email"
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {/* ── Success toast ── */}
        {lastProcessed && !simulating && (
          <div className="mb-6 bg-green-50 border border-green-200 text-green-800 text-sm px-4 py-3 rounded-lg flex items-center justify-between">
            <span>
              ✅ New email processed:{" "}
              <strong>{lastProcessed}</strong>
            </span>
            <button
              onClick={() => setLastProcessed(null)}
              className="text-green-600 hover:text-green-800"
            >
              ✕
            </button>
          </div>
        )}

        {/* ── Error message ── */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-lg">
            ⚠️ {error}
          </div>
        )}

        {/* ── Stats Row ── */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard label="Total Processed" value={stats.total} icon="📬" color="blue" />
          <StatCard label="Sales" value={stats.sales} icon="📊" color="orange" />
          <StatCard label="Calendar" value={stats.calendar} icon="🗓️" color="purple" />
          <StatCard label="Finance" value={stats.finance} icon="💰" color="green" />
        </div>

        {/* ── Email List ── */}
        {loading ? (
          // Loading skeleton
          <div className="grid gap-4 md:grid-cols-2">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="bg-white rounded-xl border border-gray-100 p-6 animate-pulse"
              >
                <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-4/5"></div>
              </div>
            ))}
          </div>
        ) : emails.length === 0 ? (
          // Empty state
          <div className="text-center py-20 text-gray-400">
            <p className="text-5xl mb-4">📭</p>
            <p className="text-lg font-medium text-gray-600">No emails processed yet</p>
            <p className="text-sm mt-1">
              Click <strong>"Simulate Email"</strong> to run the AI pipeline
            </p>
          </div>
        ) : (
          // Email grid
          <div className="grid gap-4 md:grid-cols-2">
            {emails.map((record) => (
              <EmailCard key={record.id} record={record} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

// ── Stat Card Sub-component ─────────────────────────────────────
// Defined in the same file since it's small and only used here.
// If it grew or was reused elsewhere, you'd move it to components/
function StatCard({
  label,
  value,
  icon,
  color,
}: {
  label: string;
  value: number;
  icon: string;
  color: string;
}) {
  const colorMap: Record<string, string> = {
    blue: "bg-blue-50 text-blue-600",
    orange: "bg-orange-50 text-orange-600",
    purple: "bg-purple-50 text-purple-600",
    green: "bg-green-50 text-green-600",
  };

  return (
    <div className={`rounded-xl p-4 ${colorMap[color] || colorMap.blue}`}>
      <div className="text-2xl mb-1">{icon}</div>
      <div className="text-3xl font-bold">{value}</div>
      <div className="text-xs font-medium opacity-75 mt-1">{label}</div>
    </div>
  );
}