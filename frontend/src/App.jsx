// ============================================================
// IMPORTACIONES PRINCIPALES
// ============================================================

// IMPORTAR COMPONENTES DE ENRUTAMIENTO DE REACT ROUTER
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

// IMPORTAR PÁGINAS PRINCIPALES DE LA APLICACIÓN
import Dashboard from "./paginas/dashboard/Dashboard";
import Productos from "./paginas/productos/Productos";

// IMPORTAR ESTILOS GLOBALES
import "./App.css";


// ============================================================
// COMPONENTE PRINCIPAL DE LA APLICACIÓN
// ============================================================

function App() {

    return (

        // CONTENEDOR PRINCIPAL DEL SISTEMA DE RUTEO
        <BrowserRouter>

            {/* CONTENEDOR GENERAL DE LA APLICACIÓN */}
            <div className="app">

                {/* ===================================================== */}
                {/* HEADER PRINCIPAL DEL SISTEMA */}
                {/* ===================================================== */}

                <header className="app-header">

                    {/* TÍTULO DEL SISTEMA */}
                    <h1>🍬 SGDD - Sistema de Gestión de Dulcerías</h1>

                    {/* ================================================= */}
                    {/* MENÚ DE NAVEGACIÓN PRINCIPAL */}
                    {/* ================================================= */}

                    <nav className="main-nav">

                        {/* LINK HACIA DASHBOARD */}
                        <Link to="/">Dashboard</Link>

                        {/* SEPARADOR VISUAL */}
                        <span className="separator"> | </span>

                        {/* LINK HACIA PRODUCTOS */}
                        <Link to="/productos">Productos</Link>

                    </nav>

                </header>


                {/* ===================================================== */}
                {/* LÍNEA SEPARADORA VISUAL */}
                {/* ===================================================== */}

                <hr />


                {/* ===================================================== */}
                {/* CONTENEDOR DE RUTAS PRINCIPALES */}
                {/* ===================================================== */}

                <main className="main-content">

                    <Routes>

                        {/* RUTA PRINCIPAL DEL DASHBOARD */}
                        <Route
                            path="/"
                            element={<Dashboard />}
                        />

                        {/* RUTA PARA GESTIÓN DE PRODUCTOS */}
                        <Route
                            path="/productos"
                            element={<Productos />}
                        />

                    </Routes>

                </main>

            </div>

        </BrowserRouter>
    );
}


// ============================================================
// EXPORTACIÓN DEL COMPONENTE PRINCIPAL
// ============================================================

export default App;