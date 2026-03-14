import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  HiOutlineChartBar,
  HiOutlineTable,
  HiOutlineUserCircle,
  HiOutlineLogout,
  HiOutlineMenu,
} from 'react-icons/hi';

const navLinks = [
  { to: '/', label: 'Data Penjualan', icon: HiOutlineTable },
  { to: '/predict', label: 'Prediksi', icon: HiOutlineChartBar },
  { to: '/profile', label: 'Profil', icon: HiOutlineUserCircle },
];

export default function Layout() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="drawer lg:drawer-open">
      <input id="main-drawer" type="checkbox" className="drawer-toggle" />

      {/* Main Content */}
      <div className="drawer-content flex flex-col min-h-screen">
        {/* Top Navbar (mobile) */}
        <div className="navbar bg-base-100/80 backdrop-blur-xl border-b border-base-300/50 lg:hidden sticky top-0 z-30">
          <div className="flex-none">
            <label htmlFor="main-drawer" className="btn btn-square btn-ghost">
              <HiOutlineMenu className="w-5 h-5" />
            </label>
          </div>
          <div className="flex-1">
            <span className="text-lg font-bold gradient-text">Sales Prediction</span>
          </div>
          <div className="flex-none">
            <div className="avatar placeholder">
              <div className="bg-primary text-primary-content w-8 rounded-full">
                <span className="text-xs font-bold">{user?.full_name?.charAt(0)?.toUpperCase()}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Page Content */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>

      {/* Sidebar */}
      <div className="drawer-side z-40">
        <label htmlFor="main-drawer" aria-label="close sidebar" className="drawer-overlay"></label>
        <aside className="w-72 min-h-screen bg-base-100 border-r border-base-300/50 flex flex-col">
          {/* Brand */}
          <div className="p-6 pb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                <HiOutlineChartBar className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h1 className="font-bold text-lg gradient-text">Sales AI</h1>
                <p className="text-xs text-base-content/40">Prediction System</p>
              </div>
            </div>
          </div>

          <div className="divider my-0 px-4"></div>

          {/* Nav Links */}
          <nav className="flex-1 p-4">
            <ul className="menu gap-1">
              {navLinks.map((link) => (
                <li key={link.to}>
                  <NavLink
                    to={link.to}
                    end={link.to === '/'}
                    className={({ isActive }) =>
                      `flex items-center gap-3 rounded-xl px-4 py-3 transition-all duration-200 font-medium ${
                        isActive
                          ? 'bg-primary/10 text-primary'
                          : 'text-base-content/60 hover:bg-base-200 hover:text-base-content'
                      }`
                    }
                  >
                    <link.icon className="w-5 h-5" />
                    {link.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>

          {/* User section at bottom */}
          <div className="p-4 border-t border-base-300/50">
            <div className="flex items-center gap-3 mb-3">
              <div className="avatar placeholder">
                <div className="bg-primary text-primary-content w-10 rounded-full">
                  <span className="text-sm font-bold">
                    {user?.full_name?.charAt(0)?.toUpperCase()}
                  </span>
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-sm truncate">{user?.full_name}</p>
                <p className="text-xs text-base-content/40 truncate">{user?.email}</p>
              </div>
            </div>
            <button
              className="btn btn-ghost btn-sm w-full justify-start gap-2 text-error hover:bg-error/10"
              onClick={handleLogout}
              id="logout-btn"
            >
              <HiOutlineLogout className="w-4 h-4" />
              Keluar
            </button>
          </div>
        </aside>
      </div>
    </div>
  );
}
