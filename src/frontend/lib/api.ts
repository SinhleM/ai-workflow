/**
 * lib/api.ts — API Client Layer
 *
 * This file is your frontend's "interface" to the backend.
 * Instead of scattering fetch() calls all over your components,
 * you centralise them here.
 *
 * Why centralise API calls?
 * - If your backend URL changes, you change it in ONE place
 * - Easy to add auth headers, error handling, or logging globally
 * - Components stay clean — they call a function, not fetch()
 * - Easy to mock in tests
 */

// The base URL of your FastAPI backend
// In production, this would come from an environment variable
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Represents a fully processed email record from the backend.
 * The 'export' keyword makes this type available to any component that imports it.
 */
export interface EmailRecord {
    id: string;
    timestamp: string;
    email: string;
    intent: "quote_request" | "appointment_change" | "invoice_submission";
    department: "sales" | "calendar" | "finance" | "general";
    extracted_data: {
        customer_name: string | null;
        intent: string;
        details: string;
        date: string | null;
    };
    response: string;
    status: string;
}

/**
 * Fetches all processed email records from the backend.
 *
 * Why async/await instead of .then()/.catch()?
 * Cleaner, more readable, and easier to handle errors with try/catch.
 * Both are valid JavaScript — async/await is just syntactic sugar.
 */
export async function fetchEmails(): Promise<EmailRecord[]> {
    const res = await fetch(`${API_BASE}/emails`, {
        // cache: "no-store" tells Next.js NOT to cache this response.
        // We always want fresh data on each request.
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error(`Failed to fetch emails: ${res.status}`);
    }

    const data = await res.json();
    return data.emails as EmailRecord[];
}

/**
 * Triggers the email simulation pipeline on the backend.
 * Picks a random sample email, processes it, and returns the new record.
 */
export async function simulateEmail(): Promise<EmailRecord> {
    const res = await fetch(`${API_BASE}/simulate-email`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error(`Failed to simulate email: ${res.status}`);
    }

    const data = await res.json();
    return data.record as EmailRecord;
}