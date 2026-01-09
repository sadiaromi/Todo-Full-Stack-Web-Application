// Header Component for the Todo App
import { useRouter } from 'next/router';
import AuthService from '../lib/auth';

export default function Header() {
  const router = useRouter();

  const handleLogout = () => {
    AuthService.logout();
  };

  return (
    <header className="bg-gray-800 shadow-sm border-b border-pink-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <div className="w-10 h-10 bg-gradient-to-r from-pink-500 to-purple-600 rounded-xl flex items-center justify-center mr-3 shadow-lg shadow-pink-500/20">
                <span className="text-white text-lg font-bold">T</span>
              </div>
              <h1 className="text-xl font-bold text-pink-400">Task Dashboard</h1>
            </div>
          </div>
          <div className="flex items-center">
            <button
              onClick={handleLogout}
              className="ml-4 px-5 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500/40 transition-all duration-200 shadow-lg shadow-purple-500/20 hover:shadow-purple-500/30"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
