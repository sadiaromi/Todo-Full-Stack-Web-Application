// Dashboard page for the Todo App
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import ProtectedRoute from '../components/ProtectedRoute';
import TaskManager from '../components/TaskManager';
import AuthService from '../lib/auth';

export default function Dashboard() {
  const router = useRouter();
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0 });

  const handleLogout = () => {
    AuthService.logout();
    router.push('/login');
  };

  // This would be updated by TaskManager when tasks change
  const updateStats = (tasks) => {
    const completed = tasks.filter(task => task.completed).length;
    const total = tasks.length;
    setStats({
      total,
      completed,
      pending: total - completed
    });
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 to-pink-100 py-8">
        <div className="max-w-4xl w-full px-4 sm:px-6 lg:px-8">
          {/* Main Dashboard Card */}
          <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-8 border border-pink-200 shadow-xl shadow-pink-300/20">
            {/* Header */}
            <div className="mb-8 pb-6 border-b border-pink-100">
              <div className="flex items-center justify-between">
                <div className="text-center">
                  <h1 className="text-3xl font-bold text-pink-800 mb-2">Task Dashboard</h1>
                  <p className="text-pink-600 text-sm">Organize and manage your daily tasks efficiently</p>
                </div>
                <button
                  onClick={handleLogout}
                  className="px-6 py-2.5 bg-gradient-to-r from-pink-400 to-pink-600 hover:from-pink-500 hover:to-pink-700 text-white rounded-xl text-sm font-medium transition-all duration-200 shadow-lg shadow-pink-300/20 hover:shadow-pink-400/30"
                >
                  Logout
                </button>
              </div>
            </div>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Total Tasks Card */}
              <div className="bg-pink-50 rounded-xl p-6 border border-pink-200 shadow-md text-center">
                <div>
                  <p className="text-pink-600 text-sm font-medium">Total Tasks</p>
                  <div className="text-4xl font-bold text-pink-700 mt-2">{stats.total}</div>
                </div>
              </div>

              {/* Completed Tasks Card */}
              <div className="bg-pink-50 rounded-xl p-6 border border-pink-200 shadow-md text-center">
                <div>
                  <p className="text-pink-600 text-sm font-medium">Completed</p>
                  <div className="text-4xl font-bold text-green-600 mt-2">{stats.completed}</div>
                </div>
              </div>

              {/* Pending Tasks Card */}
              <div className="bg-pink-50 rounded-xl p-6 border border-pink-200 shadow-md text-center">
                <div>
                  <p className="text-pink-600 text-sm font-medium">Pending</p>
                  <div className="text-4xl font-bold text-yellow-600 mt-2">{stats.pending}</div>
                </div>
              </div>
            </div>

            <div className="mt-6">
              <TaskManager onUpdateStats={updateStats} />
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
