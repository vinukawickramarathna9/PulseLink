import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { BellIcon, LogOutIcon, ChevronDownIcon, UserIcon } from 'lucide-react';
import LogoutConfirmModal from './modals/LogoutConfirmModal';

const Header = () => {
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const {
    user,
    logout
  } = useAuthStore();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogoutClick = () => {
    setIsDropdownOpen(false);
    setShowLogoutModal(true);
  };

  const handleLogoutConfirm = () => {
    logout();
    navigate('/login', { replace: true });
  };

  const getRoleTitle = () => {
    switch (user?.role) {
      case 'patient': return 'Patient Portal';
      case 'doctor': return 'Doctor Dashboard';
      case 'admin': return 'Admin Dashboard';
      case 'billing': return 'Billing Management';
      default: return 'PulseLink';
    }
  };

  return (
    <header className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 shadow-lg z-10">
      <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-semibold text-white">
              {getRoleTitle()}
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <button className="p-2 rounded-full text-white/80 hover:text-white hover:bg-white/20 focus:outline-none transition-all duration-200">
              <span className="sr-only">Notifications</span>
              <BellIcon className="h-6 w-6" />
            </button>
            
            <div className="relative" ref={dropdownRef}>
              <button 
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="flex items-center space-x-2 p-1.5 rounded-lg hover:bg-white/10 transition-colors focus:outline-none cursor-pointer"
              >
                {user?.avatar_url ? (
                  <img className="h-8 w-8 rounded-full border-2 border-white/30 object-cover" src={user.avatar_url} alt={user.name} />
                ) : (
                  <div className="h-8 w-8 rounded-full bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center text-white font-semibold border-2 border-white/30 shrink-0">
                    {user?.name?.charAt(0) || <UserIcon className="w-5 h-5" />}
                  </div>
                )}
                <span className="font-medium text-white hidden md:block">{user?.name}</span>
                <ChevronDownIcon className="w-4 h-4 text-white/80 hidden md:block" />
              </button>

              {isDropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg py-1 border border-slate-100 ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
                  <div className="px-4 py-2 border-b border-slate-100 md:hidden">
                    <p className="text-sm font-medium text-slate-900 truncate">{user?.name}</p>
                    <p className="text-xs text-slate-500 truncate capitalize">{user?.role}</p>
                  </div>
                  <button
                    onClick={handleLogoutClick}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2 transition-colors cursor-pointer"
                  >
                    <LogOutIcon className="w-4 h-4" />
                    <span>Log out</span>
                  </button>
                </div>
              )}
            </div>
            
          </div>
        </div>
      </div>

      <LogoutConfirmModal
        isOpen={showLogoutModal}
        onClose={() => setShowLogoutModal(false)}
        onConfirm={handleLogoutConfirm}
        userName={user?.name}
      />
    </header>
  );
};

export default Header;
