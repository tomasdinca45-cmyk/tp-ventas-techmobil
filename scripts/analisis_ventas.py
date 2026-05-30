# =============================================================================
# ANÁLISIS DE VENTAS - Escenario B
# Trabajo Práctico: Gestión Colaborativa, Control de Versiones
# Organización Empresarial - UTN TUP 2026
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# Rutas relativas para reproducibilidad en cualquier entorno
DATOS_PATH = "datos/ventas.csv"
RESULTADOS_PATH = "resultados"
os.makedirs(RESULTADOS_PATH, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. CARGA DE DATOS
# Convertimos la columna fecha a datetime para poder agrupar por mes
# -----------------------------------------------------------------------------
df = pd.read_csv(DATOS_PATH)
df["fecha"] = pd.to_datetime(df["fecha"])
df["mes"] = df["fecha"].dt.to_period("M")

print("=" * 50)
print("ANÁLISIS DE VENTAS - UTN TUP 2026")
print("=" * 50)
print(f"Registros cargados: {len(df)}")

# -----------------------------------------------------------------------------
# 2. INDICADORES GENERALES
# -----------------------------------------------------------------------------
ventas_totales = df["monto_total"].sum()
ticket_promedio = df["monto_total"].mean()
unidades_totales = df["cantidad"].sum()

ventas_por_producto = df.groupby("producto").agg(
    unidades=("cantidad", "sum"),
    ingresos=("monto_total", "sum")
).sort_values("unidades", ascending=False)

producto_top = ventas_por_producto.index[0]
unidades_top = ventas_por_producto["unidades"].iloc[0]

print(f"Ventas totales: $ {ventas_totales:,.0f}")
print(f"Ticket promedio: $ {ticket_promedio:,.0f}")
print(f"Unidades vendidas: {unidades_totales}")
print(f"Producto mas vendido: {producto_top} ({unidades_top} uds.)")

# -----------------------------------------------------------------------------
# 3. VENTAS POR MES
# Agrupamos por periodo mensual para analizar evolución temporal
# -----------------------------------------------------------------------------
ventas_mensuales = df.groupby("mes")["monto_total"].sum().reset_index()
ventas_mensuales["mes_str"] = ventas_mensuales["mes"].astype(str)

print("\nVentas por mes:")
for _, row in ventas_mensuales.iterrows():
    print(f"  {row['mes_str']}: $ {row['monto_total']:,.0f}")

# -----------------------------------------------------------------------------
# 4. GRÁFICO 1 — Evolución de Ventas Mensuales
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
colores = ["#ED7D31" if v == ventas_mensuales["monto_total"].max()
           else "#2E75B6" for v in ventas_mensuales["monto_total"]]
bars = ax.bar(ventas_mensuales["mes_str"], ventas_mensuales["monto_total"],
              color=colores, edgecolor="white")
for bar, val in zip(bars, ventas_mensuales["monto_total"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
            f"${val/1000:.0f}k", ha="center", fontsize=9, fontweight="bold")
ax.set_title("Evolución de Ventas Mensuales — TechMobil H1 2024",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Mes")
ax.set_ylabel("Monto Total (ARS)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
ax.set_ylim(0, ventas_mensuales["monto_total"].max() * 1.2)
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("resultados/ventas_mensuales.png", dpi=150, bbox_inches="tight")
plt.show()
print("Grafico 1 guardado")

# -----------------------------------------------------------------------------
# 5. GRÁFICO 2 — Top 5 Productos por Unidades Vendidas
# Barras horizontales para mejor legibilidad con nombres largos
# -----------------------------------------------------------------------------
top5 = ventas_por_producto.head(5)
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top5.index[::-1], top5["unidades"][::-1], color="#2E75B6", edgecolor="white")
for i, val in enumerate(top5["unidades"][::-1]):
    ax.text(val + 0.3, i, f"{val} uds.", va="center", fontsize=9, fontweight="bold")
ax.set_title("Top 5 Productos por Unidades Vendidas — TechMobil H1 2024",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Unidades Vendidas")
ax.set_xlim(0, top5["unidades"].max() * 1.25)
ax.grid(axis="x", linestyle="--", alpha=0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("resultados/top_productos.png", dpi=150, bbox_inches="tight")
plt.show()
print("Grafico 2 guardado")

print("\n✅ Análisis completado.")
