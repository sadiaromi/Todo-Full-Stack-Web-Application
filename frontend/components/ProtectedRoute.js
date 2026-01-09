// Protected Route Component for the Todo App
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import AuthService from '../lib/auth';

export default function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const auth = AuthService.isAuthenticated();
      setIsAuthenticated(auth);

      if (!auth) {
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  if (isAuthenticated === null) {
    // Loading state while checking authentication
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-center items-center h-96">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-pink-500"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Don't render children if not authenticated
    return null;
  }

  return children;
}
