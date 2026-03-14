import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { HiOutlineMail, HiOutlineLockClosed, HiOutlineChartBar } from 'react-icons/hi';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const result = await login(email, password);
    if (result.success) {
      navigate('/');
    } else {
      setError(result.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-base-200 px-4">
      <div className="glass-card p-8 w-full max-w-md slide-up">
        {/* Logo / branding */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 mb-4">
            <HiOutlineChartBar className="w-8 h-8 text-primary" />
          </div>
          <h1 className="text-2xl font-bold gradient-text">Sales Prediction</h1>
          <p className="text-base-content/60 mt-1 text-sm">Masuk ke akun Anda</p>
        </div>

        {/* Error alert */}
        {error && (
          <div className="alert alert-error mb-4 text-sm fade-in">
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="input input-bordered flex items-center gap-3 w-full">
            <HiOutlineMail className="w-5 h-5 text-base-content/40" />
            <input
              type="email"
              id="login-email"
              placeholder="Email"
              className="grow"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <label className="input input-bordered flex items-center gap-3 w-full">
            <HiOutlineLockClosed className="w-5 h-5 text-base-content/40" />
            <input
              type="password"
              id="login-password"
              placeholder="Password"
              className="grow"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          <button
            type="submit"
            id="login-submit"
            className="btn btn-primary w-full"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="loading loading-spinner loading-sm"></span>
            ) : (
              'Masuk'
            )}
          </button>
        </form>

        <div className="divider text-sm text-base-content/40">atau</div>

        <p className="text-center text-sm text-base-content/60">
          Belum punya akun?{' '}
          <Link to="/register" className="link link-primary font-semibold">
            Daftar sekarang
          </Link>
        </p>
      </div>
    </div>
  );
}
