const express = require("express");
const sql = require("mssql");

// CAMBIA ESTOS DATOS por los de tu SQL Server
const config = {
  user: "sa",
  password: "TU_CONTRASEÑA",
  server: "localhost",
  port: 1433,
  database: "deptmaintenance",
  options: { trustServerCertificate: true, encrypt: false },
};

const app = express();
app.use(express.static("public"));
const pool = sql.connect(config);

app.get("/api/opciones", async (req, res) => {
  try {
    const p = await pool;
    const b = await p.query("SELECT DISTINCT block_name FROM tbl_sensors_data_temp ORDER BY 1");
    const t = await p.query("SELECT DISTINCT data_type FROM tbl_sensors_data_temp ORDER BY 1");
    res.json({ bloques: b.recordset.map(r => r.block_name), tipos: t.recordset.map(r => r.data_type) });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.get("/api/datos", async (req, res) => {
  try {
    const { fecha_inicio, fecha_fin, block_name, data_type } = req.query;
    const p = await pool;
    const r = await p.request()
      .input("ini", sql.DateTime, fecha_inicio ? new Date(fecha_inicio + "T00:00:00Z") : null)
      .input("fin", sql.DateTime, fecha_fin ? new Date(fecha_fin + "T23:59:59Z") : null)
      .input("bloque", sql.VarChar(20), block_name || null)
      .input("tipo", sql.Char(4), data_type || null)
      .query(`
        SELECT TOP 1000 id_data, id_sensor, data_type, data_value, data_date, block_name
        FROM tbl_sensors_data_temp
        WHERE (@ini IS NULL OR data_date >= @ini)
          AND (@fin IS NULL OR data_date <= @fin)
          AND (@bloque IS NULL OR block_name = @bloque)
          AND (@tipo IS NULL OR data_type = @tipo)
        ORDER BY data_date DESC, block_name`);
    res.json(r.recordset);
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.listen(3000, () => console.log("Abre http://localhost:3000"));
