// Login page for the Todo App
import { useRouter } from 'next/router';
import Link from 'next/link';
import AuthService from '../lib/auth';
import AuthForm from '../components/AuthForm';

export default function Login() {
  const router = useRouter();

  const handleSubmit = async ({ email, password }) => {
    try {
      await AuthService.login(email, password);
      router.push('/'); // Redirect to dashboard after login
    } catch (err) {
      throw new Error(err.message || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 to-pink-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="mx-auto w-20 h-20 bg-gradient-to-r from-pink-400 to-pink-600 rounded-2xl flex items-center justify-center mb-6 shadow-2xl shadow-pink-300/30">
            <span className="text-white text-2xl font-bold">T</span>
          </div>
          <h2 className="text-3xl font-bold text-pink-800 mb-3 text-center">
            Welcome Back
          </h2>
          <p className="text-pink-600 text-sm text-center">Sign in to your account to continue</p>
        </div>

        <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-8 border border-pink-200 shadow-2xl shadow-pink-300/20">
          <AuthForm type="login" onSubmit={handleSubmit} />

          <div className="mt-8 text-center">
            <Link href="/signup" className="font-medium text-pink-600 hover:text-pink-800 text-base transition-colors duration-200 text-center">
              Don't have an account? Sign up
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
