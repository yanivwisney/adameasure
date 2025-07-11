import { Routes, Route } from 'react-router-dom'
import { LanguageProvider } from './contexts/LanguageContext'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Farms } from './pages/Farms'
import { Crops } from './pages/Crops'
import { Plantings } from './pages/Plantings'
import { Scheduler } from './pages/Scheduler'

function App() {
  return (
    <LanguageProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/farms" element={<Farms />} />
          <Route path="/crops" element={<Crops />} />
          <Route path="/plantings" element={<Plantings />} />
          <Route path="/scheduler" element={<Scheduler />} />
        </Routes>
      </Layout>
    </LanguageProvider>
  )
}

export default App 