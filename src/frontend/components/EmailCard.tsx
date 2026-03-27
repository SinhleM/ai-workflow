/**
 * components/EmailCard.tsx — The Visual Building Block
 *
 * This is a "presentational component" — it receives data as props
 * and renders it. It has NO side effects, NO API calls, NO state.
 *
 * Why separate components from pages?
 * - Reusability: You could use EmailCard in multiple pages
 * - Testability: Easy to test with mock data
 * - Readability: page.tsx stays clean and high-level
 * - The Single Responsibility Principle again
 *
 * "Smart components fetch data. Dumb components display it."
 */

import { EmailRecord } from "@/lib/api";

// ---------------------------------------------------------------
// Badge Configurations
// ---------------------------------------------------------------
// Maps each intent/department to a colour theme.
// Defined OUTSIDE the component so they're not recreated on every render.
// ---------------------------------------------------------------
const INTENT_STYLES: Record<string, string> = {
    quote_request: "bg-blue-100 text-blue-800 border border-blue-200",
    appointment_change: "bg-purple-100 text-purple-800 border border-purple-200",
    invoice_submission: "bg-green-100 text-green-800 border border-green-200",
};

const INTENT_LABELS: Record<string, string> = {
    quote_request: "💼 Quote Request",
    appointment_change: "📅 Appointment Change",
    invoice_submission: "🧾 Invoice Submission",
};

const DEPARTMENT_STYLES: Record<string, string> = {
    sales: "bg-orange-100 text-orange-700",
    calendar: "bg-indigo-100 text-indigo-700",
    finance: "bg-emerald-100 text-emerald-700",
    general: "bg-gray-100 text-gray-700",
};

const DEPARTMENT_ICONS: Record<string, string> = {
    sales: "📊",
    calendar: "🗓️",
    finance: "💰",
    general: "📁",
};

interface EmailCardProps {
    record: EmailRecord;
}

export default function EmailCard({ record }: EmailCardProps) {
    // Format the ISO timestamp to a readable local string
    const formattedDate = new Date(record.timestamp).toLocaleString("en-ZA", {
        dateStyle: "medium",
        timeStyle: "short",
    });

    // Truncate the email body for the preview (max 200 chars)
    const emailPreview =
        record.email.length > 200
            ? record.email.slice(0, 200) + "..."
            : record.email;

    const customerName = record.extracted_data?.customer_name;
    const details = record.extracted_data?.details;
    const date = record.extracted_data?.date;

    return (
        // The card container — white background, subtle shadow, rounded corners
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow duration-200">

            {/* ── Header Row: Intent badge + Department badge + Timestamp ── */}
            <div className="flex flex-wrap items-center gap-2 mb-4">
                {/* Intent Badge */}
                <span
                    className={`text-xs font-semibold px-3 py-1 rounded-full ${INTENT_STYLES[record.intent] || "bg-gray-100 text-gray-700"
                        }`}
                >
                    {INTENT_LABELS[record.intent] || record.intent}
                </span>

                {/* Department Badge */}
                <span
                    className={`text-xs font-medium px-3 py-1 rounded-full ${DEPARTMENT_STYLES[record.department] || "bg-gray-100 text-gray-700"
                        }`}
                >
                    {DEPARTMENT_ICONS[record.department]}{" "}
                    {record.department.charAt(0).toUpperCase() +
                        record.department.slice(1)}
                </span>

                {/* Timestamp — pushed to the right with ml-auto */}
                <span className="ml-auto text-xs text-gray-400">{formattedDate}</span>
            </div>

            {/* ── Customer Name (if extracted) ── */}
            {customerName && (
                <p className="text-sm font-semibold text-gray-800 mb-1">
                    👤 {customerName}
                </p>
            )}

            {/* ── Email Body Preview ── */}
            <div className="bg-gray-50 rounded-lg p-3 mb-4">
                <p className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-1">
                    Email Preview
                </p>
                <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                    {emailPreview}
                </p>
            </div>

            {/* ── Extracted Details Row ── */}
            {(details || date) && (
                <div className="flex flex-wrap gap-4 mb-4 text-sm">
                    {details && (
                        <div>
                            <span className="text-xs text-gray-400 uppercase tracking-wide block">
                                Details
                            </span>
                            <span className="text-gray-700">{details}</span>
                        </div>
                    )}
                    {date && (
                        <div>
                            <span className="text-xs text-gray-400 uppercase tracking-wide block">
                                Date Mentioned
                            </span>
                            <span className="text-gray-700">📆 {date}</span>
                        </div>
                    )}
                </div>
            )}

            {/* ── AI Generated Reply ── */}
            <div className="border-t border-gray-100 pt-4">
                <p className="text-xs text-gray-400 uppercase tracking-wide font-medium mb-2">
                    🤖 AI Generated Reply
                </p>
                <p className="text-sm text-gray-600 italic leading-relaxed">
                    "{record.response}"
                </p>
            </div>

            {/* ── Status Indicator ── */}
            <div className="mt-3 flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-green-400 inline-block"></span>
                <span className="text-xs text-gray-400 capitalize">{record.status}</span>
            </div>
        </div>
    );
}