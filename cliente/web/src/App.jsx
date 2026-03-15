import { Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './paginas/auth/LoginPage'
import DashboardPage from './paginas/dashboard/DashboardPage'
import ProductosPage from './paginas/productos/ProductosPage'
import POSPage from './paginas/pos/POSPage'
import InventarioPage from './paginas/inventario/InventarioPage'
import ReportesPage from './paginas/reportes/ReportesPage'
import ClientesPage from './paginas/clientes/ClientesPage'
import ProveedoresPage from './paginas/proveedores/ProveedoresPage'

function App() {
  const isAuthenticated = () => {
    return localStorage.getItem('token') !== null;
  };

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route 
        path="/dashboard" 
        element={isAuthenticated() ? <DashboardPage /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/productos" 
        element={isAuthenticated() ? <ProductosPage /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/pos" 
        element={isAuthenticated() ? <POSPage /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/inventario" 
        element={isAuthenticated() ? <InventarioPage /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/reportes" 
        element={isAuthenticated() ? <ReportesPage /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/clientes" 
        element={isAuthenticated() ? <ClientesPage /> : <Navigate to="/login" />} 
      />
      <Route 
        path="/proveedores" 
        element={isAuthenticated() ? <ProveedoresPage /> : <Navigate to="/login" />} 
      />
      <Route path="/" element={<Navigate to="/dashboard" />} />
    </Routes>
  )
}

export default App
