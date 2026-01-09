// Task Form Component for the Todo App
import { useState } from 'react';

export default function TaskForm({ onSubmit }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [completed, setCompleted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsSubmitting(true);
    try {
      await onSubmit({ title, description, completed });
      // Reset form
      setTitle('');
      setDescription('');
      setCompleted(false);
    } catch (err) {
      // Error is handled by parent component
      console.error('Failed to create task:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-pink-50 rounded-2xl p-6 border border-pink-200 shadow-md">
      <h2 className="text-xl font-semibold text-pink-800 mb-6 text-center">Add New Task</h2>
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-pink-700 mb-3">
            Task Title *
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            maxLength={100}
            className="w-full px-4 py-3 bg-white border border-pink-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-all duration-200 text-pink-900 placeholder-pink-400 text-sm"
            required
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-pink-700 mb-3">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add more details (optional)"
            maxLength={1000}
            rows="3"
            className="w-full px-4 py-3 bg-white border border-pink-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-all duration-200 text-pink-900 placeholder-pink-400 text-sm"
          />
        </div>

        <div className="flex items-center">
          <input
            id="completed"
            type="checkbox"
            checked={completed}
            onChange={(e) => setCompleted(e.target.checked)}
            className="h-5 w-5 text-pink-500 rounded focus:ring-pink-500 cursor-pointer border-pink-300 bg-white"
          />
          <label htmlFor="completed" className="ml-3 text-sm text-pink-700 cursor-pointer">
            Mark as completed
          </label>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-3.5 px-4 border border-transparent text-base font-medium rounded-xl shadow-lg text-white bg-gradient-to-r from-pink-400 to-pink-600 hover:from-pink-500 hover:to-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-400/40 disabled:opacity-50 transition-all duration-200 shadow-pink-300/20 hover:shadow-pink-400/30"
        >
          {isSubmitting ? (
            <span className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Adding Task...
            </span>
          ) : (
            'Add Task'
          )}
        </button>
      </form>
    </div>
  );
}
