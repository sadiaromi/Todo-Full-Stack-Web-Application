// Error Message Component for the Todo App
export default function ErrorMessage({ message }) {
  if (!message) return null;
  return (
    <div className="rounded-xl bg-red-50 p-4 border border-red-200 mb-6">
      <div className="text-red-700 font-medium">{message}</div>
    </div>
  );
}
