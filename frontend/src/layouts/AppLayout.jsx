import { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { ThemeToggle } from '../components/ThemeToggle';

const navItems = [
  { path: '/', label: 'Dashboard' },
  { path: '/risk', label: 'Risk Scores' },
  { path: '/dependencies', label: 'Dependencies' },
];

export function AppLayout() {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <header className="sticky top-0 z-10 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14 md:h-16">
            <div className="flex items-center gap-2 shrink-0">
              <Link to="/" className="font-semibold text-lg text-gray-900 dark:text-white">
                Construction AI Suite
              </Link>
              <span className="hidden sm:inline text-xs px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-200">
                Demo
              </span>
            </div>
            <button
              type="button"
              onClick={() => setMenuOpen((o) => !o)}
              className="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
              aria-label="Toggle menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {menuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
            <nav
              className={`absolute md:relative top-14 left-0 right-0 md:top-0 bg-white dark:bg-gray-900 md:bg-transparent border-b md:border-b-0 border-gray-200 dark:border-gray-800 md:flex items-center gap-2 md:gap-4 ${menuOpen ? 'flex flex-col py-4' : 'hidden md:flex'}`}
            >
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMenuOpen(false)}
                  className={`px-4 md:px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    location.pathname === item.path
                      ? 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
                      : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
              <div className="px-4 md:px-0 mt-2 md:mt-0">
                <ThemeToggle />
              </div>
            </nav>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
        <Outlet />
      </main>
    </div>
  );
}
