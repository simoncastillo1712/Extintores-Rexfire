-- ============================================================
--  EXTINTORES REXFIRE — Schema tablas legacy (managed=False)
--  Ejecutar en Railway MySQL Console apuntando a extintores
-- ============================================================

USE extintores;

-- 1. Categorías
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    descripcion  VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Proveedores
CREATE TABLE IF NOT EXISTS proveedor (
    id_proveedor     INT AUTO_INCREMENT PRIMARY KEY,
    rut_proveedor    VARCHAR(13)  NOT NULL UNIQUE,
    nombre_proveedor VARCHAR(200) NOT NULL UNIQUE,
    direccion        VARCHAR(150),
    telefono         VARCHAR(15),
    email            VARCHAR(100),
    fecha_registro   DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Clientes
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente     INT AUTO_INCREMENT PRIMARY KEY,
    rut_cliente    VARCHAR(15)  NOT NULL UNIQUE,
    razon_social   VARCHAR(100) NOT NULL,
    direccion      VARCHAR(150),
    telefono       VARCHAR(20),
    email          VARCHAR(100),
    fecha_registro DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Productos
CREATE TABLE IF NOT EXISTS producto (
    id_producto  INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    precio       INT          NOT NULL,
    stock        INT          NOT NULL,
    descripcion  TEXT,
    imagen       VARCHAR(100),
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Ventas
CREATE TABLE IF NOT EXISTS venta (
    id_venta       INT AUTO_INCREMENT PRIMARY KEY,
    fecha          DATETIME     NOT NULL,
    total          INT          NOT NULL,
    tipo_documento VARCHAR(7)   NOT NULL,
    origen         VARCHAR(10)  DEFAULT 'web'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Compras (a proveedores)
CREATE TABLE IF NOT EXISTS compra (
    id_compra    INT AUTO_INCREMENT PRIMARY KEY,
    fecha        DATETIME,
    total        INT UNSIGNED NOT NULL,
    estado       VARCHAR(9)   NOT NULL,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Detalle de compras
CREATE TABLE IF NOT EXISTS detalle_compra (
    id_detalle_compra INT AUTO_INCREMENT PRIMARY KEY,
    cantidad          INT UNSIGNED NOT NULL,
    precio_unitario   INT UNSIGNED NOT NULL,
    subtotal          INT UNSIGNED NOT NULL,
    id_compra         INT,
    id_producto       INT,
    FOREIGN KEY (id_compra)   REFERENCES compra(id_compra)     ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Detalle de ventas
CREATE TABLE IF NOT EXISTS detalle_venta (
    id_detalle_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_venta         INT NOT NULL,
    id_producto      INT NOT NULL,
    cantidad         INT NOT NULL,
    precio_unitario  INT NOT NULL,
    subtotal         INT NOT NULL,
    FOREIGN KEY (id_venta)    REFERENCES venta(id_venta)       ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Boletas
CREATE TABLE IF NOT EXISTS boleta (
    id_boleta     INT AUTO_INCREMENT PRIMARY KEY,
    id_venta      INT NOT NULL UNIQUE,
    numero_boleta INT NOT NULL,
    fecha_emision DATETIME NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Facturas
CREATE TABLE IF NOT EXISTS factura (
    id_factura      INT AUTO_INCREMENT PRIMARY KEY,
    id_venta        INT NOT NULL UNIQUE,
    numero_factura  INT NOT NULL,
    fecha_emision   DATETIME NOT NULL,
    id_cliente      INT,
    FOREIGN KEY (id_venta)   REFERENCES venta(id_venta)       ON DELETE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)   ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
