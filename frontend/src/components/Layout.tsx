import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  Home, 
  Building2, 
  Sprout, 
  Calendar, 
  BarChart3,
  Menu,
  X
} from 'lucide-react'
import { useState } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import { LanguageSwitcher } from './LanguageSwitcher'

interface LayoutProps {
  children: ReactNode
}

const navigation = [
  { name: 'nav.dashboard', href: '/', icon: Home },
  { name: 'nav.farms', href: '/farms', icon: Building2 },
  { name: 'nav.crops', href: '/crops', icon: Sprout },
  { name: 'nav.plantings', href: '/plantings', icon: Calendar },
  { name: 'nav.scheduler', href: '/scheduler', icon: BarChart3 },
]

export function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { t, isRTL } = useLanguage()

  return (
    <div className={`min-h-screen bg-secondary-50 ${isRTL ? 'rtl' : 'ltr'}`} dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
        <div className="fixed inset-0 bg-secondary-900/80" onClick={() => setSidebarOpen(false)} />
        <div className={`fixed inset-y-0 ${isRTL ? 'right-0' : 'left-0'} w-64 bg-white shadow-lg`}>
          <div className="flex h-16 items-center justify-between px-4">
            <h1 className="text-xl font-semibold text-primary-600">Farm Manager</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-secondary-400 hover:text-secondary-600"
            >
              <X size={24} />
            </button>
          </div>
          <nav className="px-4 py-6">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg mb-1 ${
                    isActive
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-secondary-600 hover:bg-secondary-100 hover:text-secondary-900'
                  }`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon size={20} className={isRTL ? 'ml-3' : 'mr-3'} />
                  {t(item.name)}
                </Link>
              )
            })}
            <div className="mt-6 pt-6 border-t border-secondary-200">
              <LanguageSwitcher />
            </div>
          </nav>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className={`hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col ${isRTL ? 'lg:right-0' : 'lg:left-0'}`}>
        <div className="flex flex-col flex-grow bg-white shadow-lg">
          <div className="flex h-16 items-center px-4">
            <h1 className="text-xl font-semibold text-primary-600">Farm Manager</h1>
          </div>
          <nav className="flex-1 px-4 py-6">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg mb-1 ${
                    isActive
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-secondary-600 hover:bg-secondary-100 hover:text-secondary-900'
                  }`}
                >
                  <item.icon size={20} className={isRTL ? 'ml-3' : 'mr-3'} />
                  {t(item.name)}
                </Link>
              )
            })}
            <div className="mt-6 pt-6 border-t border-secondary-200">
              <LanguageSwitcher />
            </div>
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className={isRTL ? 'lg:pr-64' : 'lg:pl-64'}>
        {/* Mobile header */}
        <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-secondary-200 bg-white px-4 shadow-sm lg:hidden">
          <button
            type="button"
            className="-m-2.5 p-2.5 text-secondary-700 lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={24} />
          </button>
          <h1 className="text-lg font-semibold text-secondary-900">Farm Management System</h1>
          <div className={isRTL ? 'mr-auto' : 'ml-auto'}>
            <LanguageSwitcher />
          </div>
        </div>

        {/* Page content */}
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
} 