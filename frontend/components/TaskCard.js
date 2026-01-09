// Task Card Component for the Todo App
import { useState } from 'react';

export default function TaskCard({ task, onEdit, onDelete, onToggleComplete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleSave = () => {
    onEdit(task.id, editTitle, editDescription, task.completed);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
  };

  const handleToggleComplete = () => {
    onToggleComplete(task.id, !task.completed);
  };

  return (
    <div className={`bg-white rounded-2xl p-6 border ${task.completed ? 'border-pink-300 bg-pink-50' : 'border-pink-200'} transition-all duration-300 hover:shadow-xl shadow-md`}>
      {isEditing ? (
        <div className="space-y-4">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full px-4 py-3 bg-white border border-pink-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-all duration-200 text-pink-900 text-sm placeholder-pink-400"
            placeholder="Task title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full px-4 py-3 bg-white border border-pink-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-all duration-200 text-pink-900 text-sm placeholder-pink-400"
            placeholder="Task description (optional)"
            rows="2"
          />
          <div className="flex space-x-3">
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 transition-all text-sm font-medium shadow-lg shadow-green-500/20"
            >
              Save Changes
            </button>
            <button
              onClick={handleCancel}
              className="px-4 py-2 bg-pink-100 hover:bg-pink-200 text-pink-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-500 transition-all text-sm font-medium"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              className="mt-1 h-5 w-5 text-pink-500 rounded focus:ring-pink-500 cursor-pointer border-pink-300 bg-white"
            />
            <div className="ml-4 flex-1">
              <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-pink-500' : 'text-pink-800'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-2 ${task.completed ? 'text-pink-400' : 'text-pink-600'} text-sm`}>
                  {task.description}
                </p>
              )}
              <div className="mt-3 flex items-center text-xs text-pink-500">
                <span>Created: {new Date(task.created_at).toLocaleString()}</span>
              </div>
            </div>
          </div>
          <div className="mt-4 flex justify-between items-center">
            <div className="flex items-center">
              {task.completed && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700 border border-green-300">
                  ✓ Completed
                </span>
              )}
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 bg-pink-100 hover:bg-pink-200 text-pink-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-500 transition-all text-sm font-medium border border-pink-300"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500 transition-all text-sm font-medium border border-red-300"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
