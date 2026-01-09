// Task Manager Component for the Todo App
import { useState, useEffect } from 'react';
import TaskForm from './TaskForm';
import TaskCard from './TaskCard';
import ApiClient from '../lib/api';
import ErrorMessage from './ErrorMessage';

const TaskManager = ({ onUpdateStats }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'completed', 'incomplete'
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTasks();
  }, [filter]);

  useEffect(() => {
    if (onUpdateStats) {
      onUpdateStats(tasks);
    }
  }, [tasks, onUpdateStats]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await ApiClient.getTasks(filter === 'all' ? null : filter);
      setTasks(data.tasks);
    } catch (err) {
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      const newTask = await ApiClient.createTask(
        taskData.title,
        taskData.description,
        taskData.completed
      );
      setTasks([newTask, ...tasks]);
    } catch (err) {
      setError(err.message || 'Failed to create task');
    }
  };

  const handleUpdateTask = async (taskId, title, description, completed) => {
    try {
      const updatedTask = await ApiClient.updateTask(
        taskId,
        title,
        description,
        completed
      );
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err) {
      setError(err.message || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await ApiClient.deleteTask(taskId);
        setTasks(tasks.filter(task => task.id !== taskId));
      } catch (err) {
        setError(err.message || 'Failed to delete task');
      }
    }
  };

  const handleToggleComplete = async (taskId, completed) => {
    try {
      const updatedTask = await ApiClient.updateTask(
        taskId,
        null,  // Don't update title
        null,  // Don't update description
        completed  // Update completion status
      );
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err) {
      setError(err.message || 'Failed to update task completion');
    }
  };

  const clearError = () => {
    setError('');
  };

  return (
    <div className="w-full">
      {error && (
        <ErrorMessage message={error} />
      )}

      {/* Task Creation Form - Add Task Section */}
      <div className="mb-8">
        <TaskForm onSubmit={handleCreateTask} />
      </div>

      {/* Filter Controls */}
      <div className="flex flex-wrap gap-3 mb-8 justify-center">
        <button
          type="button"
          className={`px-6 py-2.5 text-sm font-medium rounded-xl transition-all duration-200 ${
            filter === 'all'
              ? 'bg-gradient-to-r from-pink-400 to-pink-600 text-white shadow-lg shadow-pink-300/20'
              : 'bg-pink-100 text-pink-700 hover:bg-pink-200 border border-pink-300'
          }`}
          onClick={() => setFilter('all')}
        >
          All Tasks
        </button>
        <button
          type="button"
          className={`px-6 py-2.5 text-sm font-medium rounded-xl transition-all duration-200 ${
            filter === 'incomplete'
              ? 'bg-gradient-to-r from-pink-400 to-pink-600 text-white shadow-lg shadow-pink-300/20'
              : 'bg-pink-100 text-pink-700 hover:bg-pink-200 border border-pink-300'
          }`}
          onClick={() => setFilter('incomplete')}
        >
          Incomplete
        </button>
        <button
          type="button"
          className={`px-6 py-2.5 text-sm font-medium rounded-xl transition-all duration-200 ${
            filter === 'completed'
              ? 'bg-gradient-to-r from-pink-400 to-pink-600 text-white shadow-lg shadow-pink-300/20'
              : 'bg-pink-100 text-pink-700 hover:bg-pink-200 border border-pink-300'
          }`}
          onClick={() => setFilter('completed')}
        >
          Completed
        </button>
      </div>

      {/* Task List Section */}
      {loading ? (
        <div className="text-center py-16">
          <div className="flex justify-center mb-4">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-pink-500"></div>
          </div>
          <p className="text-pink-600 text-sm">Loading your tasks...</p>
        </div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-pink-800 font-medium text-lg mb-2">No tasks found</p>
          <p className="text-pink-600 text-sm">Create your first task to get started!</p>
        </div>
      ) : (
        <div>
          <h2 className="text-xl font-semibold text-pink-800 mb-6 text-center">
            {filter === 'all'
              ? `All Tasks (${tasks.length})`
              : filter === 'completed'
              ? `Completed Tasks (${tasks.length})`
              : `Incomplete Tasks (${tasks.length})`}
          </h2>
          <div className="space-y-4">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={handleUpdateTask}
                onDelete={handleDeleteTask}
                onToggleComplete={handleToggleComplete}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskManager;
