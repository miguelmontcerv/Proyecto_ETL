CREATE TABLE visitante (
    email VARCHAR(255) PRIMARY KEY,
    fechaPrimeraVisita DATE NOT NULL,
    fechaUltimaVisita DATE NOT NULL,
    visitasTotales INT NOT NULL,
    visitasAnioActual INT NOT NULL,
    visitasMesActual INT NOT NULL
);

CREATE TABLE estadistica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    jyv VARCHAR(255),
    Badmail VARCHAR(50),
    Baja VARCHAR(50),
    FechaEnvio DATETIME,
    FechaOpen DATETIME,
    Opens INT,
    OpensVirales INT,
    FechaClick DATETIME,
    Clicks INT,
    ClicksVirales INT,
    Links TEXT,
    IPs VARCHAR(100),
    Navegadores VARCHAR(100),
    Plataformas VARCHAR(100)
);

CREATE TABLE errores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    archivo VARCHAR(255),
    email VARCHAR(255),
    motivo VARCHAR(255),
    fechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE control_cargas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    archivo VARCHAR(255) UNIQUE,
    fechaCarga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registrosProcesados INT,
    registrosError INT
);