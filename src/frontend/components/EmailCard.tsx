import { EmailRecord } from "@/lib/api";

interface EmailCardProps {
    record: EmailRecord;
}

export default function EmailCard({ record }: EmailCardProps) {
    // Mapping departments to specific styles
    const theme = {
        sales: "border-emerald-200 bg-emerald-50 text-emerald-700",
        calendar: "border-blue-200 bg-blue-50 text-blue-700",
        finance: "border-purple-200 bg-purple-50 text-purple-700",
        general: "border-gray-200 bg-gray-50 text-gray-700",
    };

    const badgeStyle = theme[record.department] || theme.general;

    return (
        <div className="group relative bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md transition-all duration-200">
            {/* Header: Intent & Department Badge */}
            <div className="flex justify-between items-start mb-4">
                <div>
                    <span className="text-[10px] uppercase tracking-widest font-bold text-gray-400">
                        Detected Intent
                    </span>
                    <h3 className="text-lg font-bold text-gray-900 capitalize leading-tight">
                        {record.intent.replace("_", " ")}
                    </h3>
                </div>
                <span className={`text-xs font-bold px-2.5 py-1 rounded-md border ${badgeStyle}`}>
                    {record.department.toUpperCase()}
                </span>
            </div>

            {/* Raw Email Content */}
            <div className="mb-4">
                <div className="text-xs font-semibold text-gray-400 mb-1">Original Message</div>
                <p className="text-sm text-gray-600 line-clamp-3 italic leading-relaxed bg-gray-50 p-3 rounded-lg border border-gray-100">
                    "{record.email}"
                </p>
            </div>

            {/* AI Extraction Grid */}
            <div className="grid grid-cols-2 gap-3 mb-4 py-3 border-y border-gray-50">
                <div>
                    <div className="text-[10px] font-bold text-gray-400 uppercase">Customer</div>
                    <p className="text-sm font-medium text-gray-800">
                        {record.extracted_data.customer_name || "Unknown"}
                    </p>
                </div>
                <div>
                    <div className="text-[10px] font-bold text-gray-400 uppercase">Date Mentioned</div>
                    <p className="text-sm font-medium text-gray-800">
                        {record.extracted_data.date || "None"}
                    </p>
                </div>
                <div className="col-span-2">
                    <div className="text-[10px] font-bold text-gray-400 uppercase">Extracted Details</div>
                    <p className="text-sm font-medium text-gray-800 truncate">
                        {record.extracted_data.details}
                    </p>
                </div>
            </div>

            {/* AI Generated Response */}
            <div className="space-y-1">
                <div className="text-[10px] font-bold text-indigo-500 uppercase flex items-center gap-1">
                    <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-pulse"></span>
                    AI Suggested Reply
                </div>
                <p className="text-sm text-gray-800 font-medium leading-normal bg-indigo-50/50 p-3 rounded-lg border border-indigo-100">
                    {record.response}
                </p>
            </div>

            {/* Footer: Timestamp */}
            <div className="mt-4 pt-3 border-t border-gray-50 flex justify-end">
                <time className="text-[10px] text-gray-400 font-mono">
                    {new Date(record.timestamp).toLocaleString()}
                </time>
            </div>
        </div>
    );
}