// Unified Auth Form Component for the Todo App
import { useState } from 'react';

const AuthForm = ({ type = 'login', onSubmit, onCancel }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password) => {
    // At least 8 characters with uppercase, lowercase, number, and special character
    const hasMinLength = password.length >= 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    return {
      isValid: hasMinLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar,
      requirements: {
        hasMinLength,
        hasUpperCase,
        hasLowerCase,
        hasNumbers,
        hasSpecialChar
      }
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validate email
    if (!validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }

    // Validate password
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.isValid) {
      setError('Password does not meet requirements');
      return;
    }

    // For signup, validate confirm password
    if (type === 'signup') {
      if (password !== confirmPassword) {
        setError('Passwords do not match');
        return;
      }
    }

    setLoading(true);
    try {
      await onSubmit({ email, password });
    } catch (err) {
      setError(err.message || `Failed to ${type === 'login' ? 'sign in' : 'sign up'}`);
    } finally {
      setLoading(false);
    }
  };

  const isSignup = type === 'signup';

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="rounded-xl bg-red-100 p-4 border border-red-300">
          <div className="text-red-700 font-medium">{error}</div>
        </div>
      )}

      <div className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-pink-700 mb-3">
            Email Address
          </label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            className="w-full px-4 py-3 bg-white border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-all duration-200 text-pink-900 placeholder-pink-400 text-sm"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-pink-700 mb-3">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            className="w-full px-4 py-3 bg-white border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-all duration-200 text-pink-900 placeholder-pink-400 text-sm"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {type === 'signup' && (
            <div className="mt-4 space-y-2">
              <p className="text-sm font-medium text-pink-700">Password must contain:</p>
              {(() => {
                const validation = validatePassword(password);
                return (
                  <ul className="text-xs space-y-1">
                    <li className={`${validation.requirements.hasMinLength ? 'text-green-600' : 'text-red-600'}`}>
                      <span className="mr-2">{validation.requirements.hasMinLength ? '✓' : '○'}</span>
                      At least 8 characters
                    </li>
                    <li className={`${validation.requirements.hasUpperCase ? 'text-green-600' : 'text-red-600'}`}>
                      <span className="mr-2">{validation.requirements.hasUpperCase ? '✓' : '○'}</span>
                      An uppercase letter
                    </li>
                    <li className={`${validation.requirements.hasLowerCase ? 'text-green-600' : 'text-red-600'}`}>
                      <span className="mr-2">{validation.requirements.hasLowerCase ? '✓' : '○'}</span>
                      A lowercase letter
                    </li>
                    <li className={`${validation.requirements.hasNumbers ? 'text-green-600' : 'text-red-600'}`}>
                      <span className="mr-2">{validation.requirements.hasNumbers ? '✓' : '○'}</span>
                      A number
                    </li>
                    <li className={`${validation.requirements.hasSpecialChar ? 'text-green-600' : 'text-red-600'}`}>
                      <span className="mr-2">{validation.requirements.hasSpecialChar ? '✓' : '○'}</span>
                      A special character
                    </li>
                  </ul>
                );
              })()}
            </div>
          )}
        </div>

        {isSignup && (
          <div>
            <label htmlFor="confirm-password" className="block text-sm font-medium text-pink-700 mb-3">
              Confirm Password
            </label>
            <input
              id="confirm-password"
              name="confirm-password"
              type="password"
              autoComplete="current-password"
              required
              className={`w-full px-4 py-3 bg-white rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 transition-all duration-200 text-pink-900 placeholder-pink-400 text-sm ${
                confirmPassword && password !== confirmPassword
                  ? 'border border-red-500 focus:border-red-500'
                  : 'border border-pink-300 focus:border-pink-400'
              }`}
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            {confirmPassword && password !== confirmPassword && (
              <p className="mt-2 text-sm text-red-600">Passwords do not match</p>
            )}
          </div>
        )}
      </div>

      <div className="flex space-x-4">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 flex justify-center items-center py-3.5 px-4 border border-transparent text-base font-medium rounded-xl shadow-lg text-white bg-gradient-to-r from-pink-400 to-pink-600 hover:from-pink-500 hover:to-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-400/40 disabled:opacity-50 transition-all duration-200 shadow-pink-300/20 hover:shadow-pink-400/30"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              {isSignup ? 'Creating account...' : 'Signing in...'}
            </>
          ) : (
            <>
              {isSignup ? 'Sign up' : 'Sign in'}
            </>
          )}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-3.5 border border-pink-300 text-base font-medium rounded-xl text-pink-700 bg-pink-100 hover:bg-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-500 transition-all"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default AuthForm;
