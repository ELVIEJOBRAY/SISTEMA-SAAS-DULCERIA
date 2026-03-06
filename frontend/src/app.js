/**
 * SGDD - Sistema de Gestión de Dulcerías
 * app.js — Lógica principal de la SPA
 * Maneja routing, vistas y eventos del dashboard
 */

'use strict';

// ================================================================
// ESTADO GLOBAL DE LA APP
// ================================================================
const AppState = {
  currentView: 'dashboard',
  productos:   [],
  pedidos:     [],
  clientes:    [],
  inventario:  [],
};


// ================================================================
// INICIALIZACIÓN
// ================================================================
document.addEventListener('DOMContentLoaded', () => {
  // Actualizar fecha en topbar
  const topbarDate = document.getElementById('topbar-date');
  if (topbarDate) {
    topbarDate.textContent = new Date().toLocaleDateString('es-CO', {
      weekday: 'long', day: 'numeric', month: 'long',
    });
  }

  // Verificar sesión existente
  if (Auth.isLoggedIn()) {
    initApp();
  } else {
    showLogin();
  }

  // Eventos de Login
  document.getElementById('form-login').addEventListener('submit', handleLogin);

  // Sidebar toggle
  document.getElementById('sidebar-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('collapsed');
  });

  // Logout
  document.getElementById('btn-logout').addEventListener('click', handleLogout);

  // Navegación
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const view = item.dataset.view;
      if (view) navigateTo(view);
    });
  });

  // Modal
  document.getElementById('modal-close').addEventListener('click', closeModal);
  document.getElementById('modal-cancel').addEventListener('click', closeModal);
  document.getElementById('modal-overlay').addEventListener('click', (e) => {
    if (e.target === document.getElementById('modal-overlay')) closeModal();
  });

  // Bot chat
  document.getElementById('btn-enviar-chat').addEventListener('click', handleBotMessage);
  document.getElementById('chat-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleBotMessage();
    }
  });

  // Botones de acción
  document.getElementById('btn-nuevo-producto').addEventListener('click', () => showModalNuevoProducto());
  document.getElementById('btn-nuevo-pedido').addEventListener('click', () => showModalNuevoPedido());
  document.getElementById('btn-nuevo-cliente').addEventListener('click', () => showModalNuevoCliente());
  document.getElementById('btn-nuevo-lote').addEventListener('click', () => showModalNuevoLote());

  // Filtros pedidos
  document.getElementById('filtro-estado-pedido').addEventListener('change', cargarPedidos);
  document.getElementById('filtro-tipo-pedido').addEventListener('change', cargarPedidos);

  // Búsqueda productos
  document.getElementById('buscar-producto').addEventListener('input', (e) => {
    filtrarTabla('tabla-productos', e.target.value);
  });

  // Búsqueda clientes
  document.getElementById('buscar-cliente').addEventListener('input', (e) => {
    filtrarTabla('tabla-clientes', e.target.value);
  });
});


// ================================================================
// AUTH
// ================================================================
async function handleLogin(e) {
  e.preventDefault();
  const email    = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  const errorEl  = document.getElementById('login-error');
  const btnLogin = document.getElementById('btn-login');

  errorEl.classList.add('hidden');
  btnLogin.textContent = 'Iniciando sesión...';
  btnLogin.disabled = true;

  try {
    const tokenData = await ApiAuth.login(email, password);
    Auth.set(tokenData);
    await initApp();
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove('hidden');
  } finally {
    btnLogin.textContent = 'Iniciar Sesión';
    btnLogin.disabled = false;
  }
}

function handleLogout() {
  Auth.clear();
  showLogin();
  // Limpiar estado
  AppState.productos = [];
  AppState.pedidos   = [];
  AppState.clientes  = [];
}

async function initApp() {
  showApp();
  const user = Auth.getUser();
  if (user) {
    document.getElementById('sidebar-user-name').textContent = user.nombre || 'Usuario';
    document.getElementById('sidebar-user-role').textContent = user.rol   || 'empleado';
    document.getElementById('tenant-plan-badge').textContent = 'Plan Pro';
  }
  navigateTo('dashboard');
}


// ================================================================
// NAVEGACIÓN SPA
// ================================================================
function navigateTo(viewName) {
  // Ocultar todas las vistas
  document.querySelectorAll('.view').forEach(v => {
    v.classList.add('hidden');
    v.classList.remove('active');
  });

  // Desactivar nav items
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  // Activar vista
  const viewEl = document.getElementById(`view-${viewName}`);
  if (viewEl) {
    viewEl.classList.remove('hidden');
    viewEl.classList.add('active');
  }

  // Activar nav item
  const navItem = document.querySelector(`[data-view="${viewName}"]`);
  if (navItem) navItem.classList.add('active');

  // Actualizar título
  const titles = {
    dashboard: 'Dashboard', productos: 'Productos', inventario: 'Inventario',
    pedidos: 'Pedidos', clientes: 'Clientes', bot: 'Bot Conversacional', reportes: 'Reportes',
  };
  document.getElementById('page-title').textContent = titles[viewName] || viewName;

  AppState.currentView = viewName;

  // Cargar datos de la vista
  switch (viewName) {
    case 'dashboard':   cargarDashboard();   break;
    case 'productos':   cargarProductos();   break;
    case 'inventario':  cargarInventario();  break;
    case 'pedidos':     cargarPedidos();     break;
    case 'clientes':    cargarClientes();    break;
  }
}


// ================================================================
// DASHBOARD
// ================================================================
async function cargarDashboard() {
  try {
    const [pedidos, productos] = await Promise.allSettled([
      ApiPedidos.listar({ limit: 10 }),
      ApiProductos.listar({ activo: true }),
    ]);

    if (pedidos.status === 'fulfilled' && pedidos.value) {
      const lista = pedidos.value;
      AppState.pedidos = lista;

      const hoy = new Date().toDateString();
      const pedidosHoy = lista.filter(p => new Date(p.fecha_pedido).toDateString() === hoy);
      const ventasHoy  = pedidosHoy.reduce((s, p) => s + parseFloat(p.total), 0);
      const botHoy     = pedidosHoy.filter(p => p.tipo_pedido === 'bot').length;

      document.getElementById('kpi-pedidos-hoy').textContent = pedidosHoy.length;
      document.getElementById('kpi-ventas-hoy').textContent  = formatCurrency(ventasHoy);
      document.getElementById('kpi-bot-pedidos').textContent = botHoy;

      renderTablaPedidosRecientes(lista.slice(0, 6));
    }

    if (productos.status === 'fulfilled' && productos.value) {
      AppState.productos = productos.value;
      // Simulación stock bajo
      const stockBajo = Math.floor(Math.random() * 4);
      document.getElementById('kpi-stock-bajo').textContent = stockBajo;

      if (stockBajo > 0) {
        const notifEl = document.getElementById('notif-vencimientos');
        notifEl.textContent = `${stockBajo} alertas`;
        notifEl.classList.add('visible');
      }
    }

    cargarVencimientosDemo();

  } catch (err) {
    console.warn('[Dashboard] Error cargando datos:', err.message);
    renderDashboardDemo();
  }
}

function renderDashboardDemo() {
  document.getElementById('kpi-pedidos-hoy').textContent = '12';
  document.getElementById('kpi-ventas-hoy').textContent  = formatCurrency(485000);
  document.getElementById('kpi-bot-pedidos').textContent = '4';
  document.getElementById('kpi-stock-bajo').textContent  = '2';

  const pedidosDemo = [
    { pedido_id: 'P-001', tipo_pedido: 'manual', estado: 'entregado', total: 45000, fecha_pedido: new Date().toISOString() },
    { pedido_id: 'P-002', tipo_pedido: 'bot',    estado: 'confirmado', total: 78000, fecha_pedido: new Date().toISOString() },
    { pedido_id: 'P-003', tipo_pedido: 'manual', estado: 'pendiente', total: 32000, fecha_pedido: new Date().toISOString() },
  ];
  renderTablaPedidosRecientes(pedidosDemo);
  cargarVencimientosDemo();
}

function renderTablaPedidosRecientes(pedidos) {
  const tbody = document.querySelector('#tabla-pedidos-recientes tbody');
  if (!tbody) return;
  if (!pedidos.length) {
    tbody.innerHTML = '<tr><td colspan="5" class="table-empty">No hay pedidos recientes.</td></tr>';
    return;
  }
  tbody.innerHTML = pedidos.map(p => `
    <tr>
      <td><code>${String(p.pedido_id).slice(-6).toUpperCase()}</code></td>
      <td>${estadoBadge(p.tipo_pedido)}</td>
      <td>${estadoBadge(p.estado)}</td>
      <td>${formatCurrency(p.total)}</td>
      <td>${formatDateTime(p.fecha_pedido)}</td>
    </tr>
  `).join('');
}

function cargarVencimientosDemo() {
  const container = document.getElementById('lista-vencimientos');
  if (!container) return;
  const items = [
    { nombre: 'Chocolates Jet 24g', dias: 5, cantidad: 20 },
    { nombre: 'Gomitas Haribo 200g', dias: 12, cantidad: 45 },
    { nombre: 'Caramelos Colombina', dias: 28, cantidad: 100 },
  ];
  container.innerHTML = items.map(i => `
    <div class="venc-item ${i.dias <= 7 ? 'critico' : ''}">
      <div>
        <div class="venc-nombre">${i.nombre}</div>
        <div class="venc-dias">Cantidad: ${i.cantidad} unidades</div>
      </div>
      <span class="badge ${i.dias <= 7 ? 'badge-red' : 'badge-yellow'}">${i.dias} días</span>
    </div>
  `).join('');
}


// ================================================================
// PRODUCTOS
// ================================================================
async function cargarProductos() {
  try {
    const productos = await ApiProductos.listar();
    AppState.productos = productos || [];
    renderTablaProductos(AppState.productos);
  } catch (err) {
    console.warn('[Productos] Usando datos demo:', err.message);
    renderTablaProductos(getProductosDemo());
  }
}

function getProductosDemo() {
  return [
    { producto_id: '1', nombre: 'Chocolate Jet 24g',     tipo_producto: 'chocolate', marca: 'Jet',       precio_minorista: 1500, precio_mayorista: 1200, sku: 'JET-001', activo: true },
    { producto_id: '2', nombre: 'Gomitas Haribo 200g',   tipo_producto: 'gomita',    marca: 'Haribo',     precio_minorista: 4500, precio_mayorista: 3800, sku: 'HAR-001', activo: true },
    { producto_id: '3', nombre: 'Bon Bon Bum Fresa',     tipo_producto: 'paleta',    marca: 'Colombina',  precio_minorista: 800,  precio_mayorista: 600,  sku: 'BBB-001', activo: true },
    { producto_id: '4', nombre: 'Caramelos Halls Menta', tipo_producto: 'caramelo',  marca: 'Halls',      precio_minorista: 2200, precio_mayorista: 1800, sku: 'HLS-001', activo: false },
    { producto_id: '5', nombre: 'Trident Menta 12u',     tipo_producto: 'chicle',    marca: 'Trident',    precio_minorista: 1800, precio_mayorista: 1400, sku: 'TRI-001', activo: true },
  ];
}

function renderTablaProductos(productos) {
  const tbody = document.querySelector('#tabla-productos tbody');
  const empty = document.getElementById('productos-empty');
  if (!tbody) return;

  if (!productos.length) {
    tbody.innerHTML = '';
    empty && empty.classList.remove('hidden');
    return;
  }

  empty && empty.classList.add('hidden');
  tbody.innerHTML = productos.map(p => `
    <tr>
      <td><strong>${p.nombre}</strong></td>
      <td>${p.tipo_producto}</td>
      <td>${p.marca || '—'}</td>
      <td>${formatCurrency(p.precio_minorista)}</td>
      <td>${p.precio_mayorista ? formatCurrency(p.precio_mayorista) : '—'}</td>
      <td><code>${p.sku || '—'}</code></td>
      <td>${estadoBadge(p.activo ? 'activo' : 'suspendido')}</td>
      <td>
        <button class="btn-icon" onclick="editarProducto('${p.producto_id}')" title="Editar">✏️</button>
        <button class="btn-icon" onclick="eliminarProducto('${p.producto_id}')" title="Eliminar">🗑️</button>
      </td>
    </tr>
  `).join('');
}

function editarProducto(id) {
  const p = AppState.productos.find(x => x.producto_id === id);
  if (!p) return;
  openModal(`Editar: ${p.nombre}`, `
    <div class="form-group">
      <label>Precio Minorista (COP)</label>
      <input type="number" id="edit-precio-min" value="${p.precio_minorista}" />
    </div>
    <div class="form-group">
      <label>Precio Mayorista (COP)</label>
      <input type="number" id="edit-precio-may" value="${p.precio_mayorista || ''}" />
    </div>
    <div class="form-group">
      <label>Estado</label>
      <select id="edit-activo">
        <option value="true"  ${p.activo ? 'selected' : ''}>Activo</option>
        <option value="false" ${!p.activo ? 'selected' : ''}>Inactivo</option>
      </select>
    </div>
  `, async () => {
    try {
      const data = {
        precio_minorista: parseFloat(document.getElementById('edit-precio-min').value),
        precio_mayorista: parseFloat(document.getElementById('edit-precio-may').value) || null,
        activo: document.getElementById('edit-activo').value === 'true',
      };
      await ApiProductos.actualizar(id, data);
      closeModal();
      cargarProductos();
    } catch {
      // Demo mode: solo actualizar localmente
      const idx = AppState.productos.findIndex(x => x.producto_id === id);
      if (idx !== -1) {
        AppState.productos[idx].precio_minorista = parseFloat(document.getElementById('edit-precio-min').value);
        renderTablaProductos(AppState.productos);
      }
      closeModal();
    }
  });
}

function eliminarProducto(id) {
  const p = AppState.productos.find(x => x.producto_id === id);
  openModal('Confirmar eliminación', `
    <p>¿Desactivar el producto <strong>${p?.nombre || id}</strong>?</p>
    <p class="text-muted mt-2">El producto no se eliminará permanentemente, solo se desactivará.</p>
  `, async () => {
    try {
      await ApiProductos.eliminar(id);
    } catch { /* demo */ }
    AppState.productos = AppState.productos.filter(x => x.producto_id !== id);
    renderTablaProductos(AppState.productos);
    closeModal();
  });
}

function showModalNuevoProducto() {
  openModal('Nuevo Producto', `
    <div class="form-group">
      <label>Nombre *</label>
      <input type="text" id="np-nombre" placeholder="Ej: Chocolate Jet 24g" />
    </div>
    <div class="form-group">
      <label>Tipo de Producto *</label>
      <select id="np-tipo">
        <option value="">Seleccionar...</option>
        <option value="chocolate">Chocolate</option>
        <option value="gomita">Gomita</option>
        <option value="caramelo">Caramelo</option>
        <option value="paleta">Paleta</option>
        <option value="chicle">Chicle</option>
        <option value="galleta">Galleta</option>
        <option value="snack">Snack</option>
      </select>
    </div>
    <div class="form-group">
      <label>Marca</label>
      <input type="text" id="np-marca" placeholder="Ej: Colombina" />
    </div>
    <div class="form-group">
      <label>Precio Minorista (COP) *</label>
      <input type="number" id="np-precio-min" min="0" placeholder="1500" />
    </div>
    <div class="form-group">
      <label>Precio Mayorista (COP)</label>
      <input type="number" id="np-precio-may" min="0" placeholder="1200" />
    </div>
    <div class="form-group">
      <label>SKU</label>
      <input type="text" id="np-sku" placeholder="JET-001" />
    </div>
  `, async () => {
    const nombre = document.getElementById('np-nombre').value.trim();
    const tipo   = document.getElementById('np-tipo').value;
    const pMin   = parseFloat(document.getElementById('np-precio-min').value);

    if (!nombre || !tipo || isNaN(pMin)) {
      alert('Por favor completa los campos obligatorios (*)');
      return;
    }

    const data = {
      nombre,
      tipo_producto:    tipo,
      marca:            document.getElementById('np-marca').value || null,
      precio_minorista: pMin,
      precio_mayorista: parseFloat(document.getElementById('np-precio-may').value) || null,
      sku:              document.getElementById('np-sku').value || null,
    };

    try {
      await ApiProductos.crear(data);
    } catch {
      // Demo: agregar localmente
      AppState.productos.push({ ...data, producto_id: Date.now().toString(), activo: true });
    }

    closeModal();
    cargarProductos();
  });
}


// ================================================================
// INVENTARIO
// ================================================================
async function cargarInventario() {
  renderTablaInventarioDemo();
}

function renderTablaInventarioDemo() {
  const tbody = document.querySelector('#tabla-inventario tbody');
  if (!tbody) return;
  const data = [
    { nombre: 'Chocolate Jet 24g',     stock: 180, min: 20, lote: 'L-2024-001', venc: '2025-03-15', cant_lote: 80,  estado: 'ok' },
    { nombre: 'Gomitas Haribo 200g',   stock: 45,  min: 30, lote: 'L-2024-002', venc: '2025-05-20', cant_lote: 45,  estado: 'ok' },
    { nombre: 'Bon Bon Bum Fresa',     stock: 320, min: 50, lote: 'L-2024-003', venc: '2026-01-10', cant_lote: 150, estado: 'ok' },
    { nombre: 'Caramelos Halls',       stock: 18,  min: 30, lote: 'L-2024-004', venc: '2025-02-05', cant_lote: 18,  estado: 'bajo' },
    { nombre: 'Trident Menta 12u',     stock: 90,  min: 20, lote: 'L-2024-005', venc: '2025-08-30', cant_lote: 90,  estado: 'ok' },
  ];

  tbody.innerHTML = data.map(d => `
    <tr>
      <td><strong>${d.nombre}</strong></td>
      <td>
        <span class="${d.stock <= d.min ? 'badge badge-red' : 'badge badge-green'}">${d.stock} u.</span>
      </td>
      <td>${d.min} u.</td>
      <td><code>${d.lote}</code></td>
      <td>${d.venc}</td>
      <td>${d.cant_lote} u.</td>
      <td>${d.estado === 'bajo' ? '<span class="badge badge-red">⚠️ Bajo</span>' : '<span class="badge badge-green">OK</span>'}</td>
    </tr>
  `).join('');
}

function showModalNuevoLote() {
  const opciones = (AppState.productos.length ? AppState.productos : getProductosDemo())
    .filter(p => p.activo)
    .map(p => `<option value="${p.producto_id}">${p.nombre}</option>`)
    .join('');

  openModal('Registrar Nuevo Lote', `
    <div class="form-group">
      <label>Producto *</label>
      <select id="lote-producto">${opciones}</select>
    </div>
    <div class="form-group">
      <label>N° Lote</label>
      <input type="text" id="lote-numero" placeholder="L-2024-006" />
    </div>
    <div class="form-group">
      <label>Fecha de Ingreso *</label>
      <input type="date" id="lote-ingreso" value="${new Date().toISOString().split('T')[0]}" />
    </div>
    <div class="form-group">
      <label>Fecha de Vencimiento *</label>
      <input type="date" id="lote-venc" />
    </div>
    <div class="form-group">
      <label>Cantidad *</label>
      <input type="number" id="lote-cantidad" min="1" placeholder="100" />
    </div>
  `, () => {
    closeModal();
    cargarInventario();
  });
}


// ================================================================
// PEDIDOS
// ================================================================
async function cargarPedidos() {
  const estado = document.getElementById('filtro-estado-pedido').value;
  const tipo   = document.getElementById('filtro-tipo-pedido').value;

  try {
    const pedidos = await ApiPedidos.listar({ estado: estado || null, tipo_pedido: tipo || null });
    AppState.pedidos = pedidos || [];
    renderTablaPedidos(AppState.pedidos);
  } catch {
    renderTablaPedidos(getPedidosDemo());
  }
}

function getPedidosDemo() {
  return [
    { pedido_id: 'ped-001', cliente_id: null, tipo_pedido: 'manual', estado: 'entregado', total: 45000,  fecha_pedido: new Date().toISOString() },
    { pedido_id: 'ped-002', cliente_id: null, tipo_pedido: 'bot',    estado: 'confirmado', total: 78000, fecha_pedido: new Date().toISOString() },
    { pedido_id: 'ped-003', cliente_id: null, tipo_pedido: 'manual', estado: 'pendiente',  total: 32000, fecha_pedido: new Date().toISOString() },
    { pedido_id: 'ped-004', cliente_id: null, tipo_pedido: 'bot',    estado: 'cancelado',  total: 12000, fecha_pedido: new Date().toISOString() },
  ];
}

function renderTablaPedidos(pedidos) {
  const tbody = document.querySelector('#tabla-pedidos tbody');
  if (!tbody) return;
  if (!pedidos.length) {
    tbody.innerHTML = '<tr><td colspan="7" class="table-empty">No hay pedidos.</td></tr>';
    return;
  }
  tbody.innerHTML = pedidos.map(p => `
    <tr>
      <td><code>${String(p.pedido_id).slice(-6).toUpperCase()}</code></td>
      <td>${p.cliente_id ? p.cliente_id.slice(-6).toUpperCase() : '<span class="text-muted">Sin cliente</span>'}</td>
      <td>${estadoBadge(p.tipo_pedido)}</td>
      <td>${estadoBadge(p.estado)}</td>
      <td>${formatCurrency(p.total)}</td>
      <td>${formatDateTime(p.fecha_pedido)}</td>
      <td>
        <button class="btn-icon" onclick="cambiarEstadoPedido('${p.pedido_id}')" title="Cambiar estado">🔄</button>
      </td>
    </tr>
  `).join('');
}

function cambiarEstadoPedido(id) {
  openModal('Actualizar Estado', `
    <div class="form-group">
      <label>Nuevo estado</label>
      <select id="nuevo-estado-pedido">
        <option value="pendiente">Pendiente</option>
        <option value="confirmado">Confirmado</option>
        <option value="entregado">Entregado</option>
        <option value="cancelado">Cancelado</option>
      </select>
    </div>
  `, async () => {
    const estado = document.getElementById('nuevo-estado-pedido').value;
    try {
      await ApiPedidos.actualizarEstado(id, estado);
    } catch { /* demo */ }
    closeModal();
    cargarPedidos();
  });
}

function showModalNuevoPedido() {
  const opProductos = (AppState.productos.length ? AppState.productos : getProductosDemo())
    .filter(p => p.activo)
    .map(p => `<option value="${p.producto_id}" data-precio="${p.precio_minorista}">${p.nombre} - ${formatCurrency(p.precio_minorista)}</option>`)
    .join('');

  openModal('Nuevo Pedido Manual', `
    <div class="form-group">
      <label>Producto *</label>
      <select id="ped-producto">${opProductos}</select>
    </div>
    <div class="form-group">
      <label>Cantidad *</label>
      <input type="number" id="ped-cantidad" min="1" value="1" />
    </div>
    <div class="form-group">
      <label>Notas</label>
      <input type="text" id="ped-notas" placeholder="Observaciones del pedido..." />
    </div>
  `, () => {
    closeModal();
    cargarPedidos();
  });
}


// ================================================================
// CLIENTES
// ================================================================
async function cargarClientes() {
  try {
    const clientes = await ApiClientes.listar();
    AppState.clientes = clientes || [];
    renderTablaClientes(AppState.clientes);
  } catch {
    renderTablaClientes(getClientesDemo());
  }
}

function getClientesDemo() {
  return [
    { cliente_id: 'c1', nombre: 'María García',     telefono: '+57 310 123 4567', tipo_cliente: 'minorista' },
    { cliente_id: 'c2', nombre: 'Distribuidora ABC', telefono: '+57 320 987 6543', tipo_cliente: 'mayorista' },
    { cliente_id: 'c3', nombre: 'Juan Pérez',        telefono: '+57 315 456 7890', tipo_cliente: 'minorista' },
  ];
}

function renderTablaClientes(clientes) {
  const tbody = document.querySelector('#tabla-clientes tbody');
  if (!tbody) return;
  tbody.innerHTML = clientes.map(c => `
    <tr>
      <td>${c.nombre}</td>
      <td>${c.telefono || '—'}</td>
      <td>${estadoBadge(c.tipo_cliente)}</td>
      <td>
        <button class="btn-icon" title="Ver pedidos">🛒</button>
      </td>
    </tr>
  `).join('');
}

function showModalNuevoCliente() {
  openModal('Nuevo Cliente', `
    <div class="form-group">
      <label>Nombre *</label>
      <input type="text" id="cli-nombre" placeholder="Nombre completo" />
    </div>
    <div class="form-group">
      <label>Teléfono</label>
      <input type="tel" id="cli-tel" placeholder="+57 300 000 0000" />
    </div>
    <div class="form-group">
      <label>Email</label>
      <input type="email" id="cli-email" placeholder="cliente@email.com" />
    </div>
    <div class="form-group">
      <label>Tipo</label>
      <select id="cli-tipo">
        <option value="minorista">Minorista</option>
        <option value="mayorista">Mayorista</option>
      </select>
    </div>
  `, async () => {
    const nombre = document.getElementById('cli-nombre').value.trim();
    if (!nombre) { alert('El nombre es obligatorio'); return; }
    try {
      await ApiClientes.crear({
        nombre, telefono: document.getElementById('cli-tel').value || null,
        email: document.getElementById('cli-email').value || null,
        tipo_cliente: document.getElementById('cli-tipo').value,
      });
    } catch {
      AppState.clientes.push({ cliente_id: Date.now().toString(), nombre, tipo_cliente: 'minorista' });
    }
    closeModal();
    cargarClientes();
  });
}


// ================================================================
// BOT CONVERSACIONAL
// ================================================================
async function handleBotMessage() {
  const input   = document.getElementById('chat-input');
  const mensaje = input.value.trim();
  if (!mensaje) return;

  input.value = '';
  appendChatMessage(mensaje, 'user');

  // Mostrar indicador de escritura
  const typingId = appendChatMessage('...', 'bot typing');

  try {
    const res = await ApiBot.enviarMensaje(mensaje);
    removeChatMessage(typingId);
    appendChatMessage(res.respuesta, 'bot');
    actualizarMetricasBot(res);
  } catch (err) {
    removeChatMessage(typingId);
    // Procesamiento demo local con motor NLP simulado
    const { respuesta, metrics } = procesarMensajeDemo(mensaje);
    appendChatMessage(respuesta, 'bot');
    actualizarMetricasBot(metrics);
  }
}

function procesarMensajeDemo(mensaje) {
  const lower = mensaje.toLowerCase();
  let intencion = 'desconocida';
  let confianza = 0.65;
  let respuesta = 'No entendí bien tu solicitud. ¿Puedes ser más específico? Ej: "Quiero 5 chocolates Jet"';
  let entidades = {};
  let escalado = false;

  // Saludo
  if (/^(hola|buenas?|buenos?|hey|saludos?)/.test(lower)) {
    intencion = 'saludo'; confianza = 0.97;
    respuesta = '¡Hola! Bienvenido a SGDD 🍬 ¿En qué te puedo ayudar?';
  }
  // Pedido
  else if (/(quiero|dame|necesito|pedir|ordenar)/.test(lower)) {
    intencion = 'crear_pedido'; confianza = 0.92;
    const cantMatch = lower.match(/(\d+)\s*(chocolates?|gomitas?|caramelos?|paletas?|dulces?)/);
    if (cantMatch) {
      entidades = { cantidad: parseInt(cantMatch[1]), tipo: cantMatch[2].replace(/s$/, '') };
      respuesta = `✅ Entendido, ${cantMatch[1]} ${cantMatch[2]}. ¿Confirmas el pedido?`;
    } else {
      respuesta = '¿Qué producto deseas? Ej: "Quiero 10 chocolates Jet"';
    }
  }
  // Precio
  else if (/(precio|cuesta|cuánto|cuanto|valor)/.test(lower)) {
    intencion = 'consultar_precio'; confianza = 0.88;
    respuesta = 'Puedes ver todos los precios en la sección de Productos. ¿Cuál te interesa específicamente?';
  }
  // Evento
  else if (/(evento|fiesta|piñata|cumpleaños|cotizaci)/.test(lower)) {
    intencion = 'cotizacion_evento'; confianza = 0.91;
    respuesta = '🎉 Para eventos envíanos el listado de productos. ¡Te respondemos en menos de 1 hora!';
  }
  // Despedida
  else if (/(chao|adios|hasta\s*luego|gracias)/.test(lower)) {
    intencion = 'despedida'; confianza = 0.95;
    respuesta = '¡Hasta luego! Que tengas un excelente día. 🍭';
  }

  if (confianza < 0.75) escalado = true;

  return {
    respuesta,
    metrics: {
      intencion, confianza, escalado, entidades,
      tiempo_ms: Math.floor(Math.random() * 120) + 40,
    },
  };
}

function actualizarMetricasBot(res) {
  const int = res.intencion || '—';
  const conf = res.confianza || 0;

  document.getElementById('metric-intencion').textContent = int.replace('_', ' ');
  document.getElementById('metric-intencion').className   = 'badge badge-purple';

  document.getElementById('metric-confianza').textContent = `${(conf * 100).toFixed(0)}%`;
  document.getElementById('progress-confianza').style.width = `${conf * 100}%`;

  const tiempoEl = document.getElementById('metric-tiempo');
  tiempoEl.textContent = `${res.tiempo_ms || '—'} ms`;
  tiempoEl.className   = (res.tiempo_ms || 0) > 3000 ? 'badge badge-red' : 'badge badge-blue';

  const escEl = document.getElementById('metric-escalado');
  escEl.textContent = res.escalado ? 'Sí (humano)' : 'No';
  escEl.className   = `badge ${res.escalado ? 'badge-yellow' : 'badge-green'}`;

  // Entidades
  const e = res.entidades || {};
  document.getElementById('entity-producto').textContent = e.producto || '—';
  document.getElementById('entity-cantidad').textContent = e.cantidad || '—';
  document.getElementById('entity-marca').textContent    = e.marca    || '—';
}

let _chatMsgCounter = 0;

function appendChatMessage(text, type) {
  const id = `msg-${++_chatMsgCounter}`;
  const container = document.getElementById('chat-messages');
  const cls = type.includes('user') ? 'user' : type.includes('error') ? 'error' : 'bot';
  const div = document.createElement('div');
  div.className = `chat-msg ${cls}`;
  div.id = id;
  div.innerHTML = `<div class="msg-bubble">${text}</div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeChatMessage(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}


// ================================================================
// MODAL GENÉRICO
// ================================================================
let _modalConfirmCallback = null;

function openModal(title, bodyHtml, onConfirm) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = bodyHtml;
  _modalConfirmCallback = onConfirm;
  document.getElementById('modal-overlay').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
  _modalConfirmCallback = null;
}

document.getElementById('modal-confirm').addEventListener('click', () => {
  if (_modalConfirmCallback) _modalConfirmCallback();
});


// ================================================================
// UTILIDADES
// ================================================================
function filtrarTabla(tablaId, query) {
  const tbody = document.querySelector(`#${tablaId} tbody`);
  if (!tbody) return;
  const rows = tbody.querySelectorAll('tr');
  const q = query.toLowerCase();
  rows.forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}
