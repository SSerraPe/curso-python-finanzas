"""Generación de informes: Excel formateado (xlsxwriter) y PDF (fpdf2)."""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
         "octubre", "noviembre", "diciembre"]


# --------------------------------------------------------------------------- Excel
def _hoja_tabla(xw, df: pd.DataFrame, hoja: str, titulo: str, fmt_cols: dict[str, str], index=True,
                col_semaforo: str | None = None):
    """Escribe una tabla con título, formatos por columna, paneles fijos y autofiltro."""
    wb = xw.book
    df.to_excel(xw, sheet_name=hoja, startrow=2, index=index)
    ws = xw.sheets[hoja]
    f_tit = wb.add_format({"bold": True, "font_size": 14, "font_color": "#1F4E79"})
    formatos = {
        "eur": wb.add_format({"num_format": '#,##0 "€";[Red]-#,##0 "€"'}),
        "pct": wb.add_format({"num_format": "0.0%"}),
        "int": wb.add_format({"num_format": "#,##0"}),
        "txt": wb.add_format({}),
    }
    ws.write(0, 0, titulo, f_tit)
    desplaz = 1 if index else 0
    nombre_index = df.index.name if index else None
    ws.set_column(0, 0, 28 if index else 14)
    for j, col in enumerate(df.columns):
        ws.set_column(j + desplaz, j + desplaz, max(14, len(str(col)) + 2),
                      formatos.get(fmt_cols.get(col, "txt")))
    ws.freeze_panes(3, desplaz)
    ws.autofilter(2, 0, 2 + len(df), len(df.columns) + desplaz - 1)
    if col_semaforo and col_semaforo in df.columns:
        j = list(df.columns).index(col_semaforo) + desplaz
        verde = wb.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})
        rojo = wb.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})
        ambar = wb.add_format({"bg_color": "#FFEB9C", "font_color": "#9C5700"})
        rango = (3, j, 2 + len(df), j)
        for valor, fmt in [("OK", verde), ("Favorable", verde), ("KO", rojo), ("Desfavorable", rojo),
                           ("AVISO", ambar)]:
            ws.conditional_format(*rango, {"type": "cell", "criteria": "==", "value": f'"{valor}"',
                                           "format": fmt})
    _ = nombre_index
    return ws


def escribir_excel_cierre(res: dict, ruta: Path, canal: str | None = None) -> Path:
    """Excel del cierre. Si `canal` se indica, solo incluye ese canal (para enviar
    a cada responsable)."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    mes = res["mes"]
    fmt_res = {c: "eur" for c in res["resultado_ytd"].columns}
    fmt_res.update({c: "pct" for c in res["resultado_ytd"].columns if "%" in c})
    fmt_rvp = {"Real": "eur", "Presupuesto": "eur", "Desviación": "eur", "Desviación %": "pct"}

    def filtra(df, por_indice=True):
        if canal is None:
            return df
        return df.loc[[canal]] if por_indice else df[df["canal"] == canal]

    with pd.ExcelWriter(ruta, engine="xlsxwriter") as xw:
        _hoja_tabla(xw, filtra(res["resultado_ytd"]), "Resultado YTD",
                    f"Cuenta técnica acumulada enero-{MESES[mes - 1]} 2025", fmt_res)
        _hoja_tabla(xw, filtra(res["resultado_mes"]), "Resultado mes",
                    f"Cuenta técnica de {MESES[mes - 1]} 2025", fmt_res)
        _hoja_tabla(xw, filtra(res["rvp_ytd"], False), "Real vs Ppto YTD",
                    "Real vs presupuesto (acumulado)", fmt_rvp, index=False, col_semaforo="Valoración")
        if canal is None:
            _hoja_tabla(xw, res["controles"], "Controles", "Controles de calidad de datos", {},
                        index=False, col_semaforo="resultado")
        # Gráfico nativo de Excel: margen técnico YTD por canal
        ws = xw.sheets["Resultado YTD"]
        t = filtra(res["resultado_ytd"])
        col_margen = list(t.columns).index("Margen técnico") + 1
        chart = xw.book.add_chart({"type": "column"})
        n = len(t) - (1 if canal is None else 0)   # sin la fila Total
        chart.add_series({"name": "Margen técnico YTD",
                          "categories": ["Resultado YTD", 3, 0, 2 + n, 0],
                          "values": ["Resultado YTD", 3, col_margen, 2 + n, col_margen],
                          "fill": {"color": "#1F4E79"}, "invert_if_negative": True})
        chart.set_title({"name": "Margen técnico acumulado por canal"})
        chart.set_legend({"none": True})
        chart.set_y_axis({"num_format": '#,##0 "€"'})
        ws.insert_chart(len(t) + 5, 1, chart, {"x_scale": 1.3, "y_scale": 1.1})
    return ruta


# --------------------------------------------------------------------------- PDF
def grafico_margen(res: dict, ruta_png: Path) -> Path:
    t = res["resultado_ytd"].drop(index="Total")
    fig, ax = plt.subplots(figsize=(7, 3.2))
    colores = ["#1F4E79" if v >= 0 else "#C0392B" for v in t["Margen técnico"]]
    ax.bar(t.index, t["Margen técnico"] / 1e6, color=colores)
    ax.axhline(0, color="black", lw=0.8)
    ax.margins(y=0.2)
    ax.set_ylabel("M€")
    ax.set_title("Margen técnico acumulado por canal")
    for i, v in enumerate(t["Ratio combinado %"]):
        ax.annotate(f"RC {v:.0%}", (i, t["Margen técnico"].iloc[i] / 1e6), ha="center",
                    va="bottom" if t["Margen técnico"].iloc[i] >= 0 else "top", fontsize=9)
    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)
    return ruta_png


def generar_pdf_cierre(res: dict, ruta: Path) -> Path:
    """PDF de una página: titular, tabla resumen, gráfico y estado de controles."""
    from fpdf import FPDF

    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    mes = res["mes"]
    fuente = Path(matplotlib.get_data_path()) / "fonts" / "ttf"   # DejaVu viene con matplotlib
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.add_font("DejaVu", "", str(fuente / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", str(fuente / "DejaVuSans-Bold.ttf"))

    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(31, 78, 121)
    pdf.cell(0, 10, f"Cierre de {MESES[mes - 1]} 2025 · Ramo Autos", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", 10)
    t = res["resultado_ytd"]
    tot = t.loc["Total"]
    rvp = res["rvp_ytd"]
    desv_margen = rvp[(rvp["canal"] == "Total") & (rvp["concepto"] == "Margen técnico")]["Desviación"].iloc[0]
    peor = t.drop(index="Total")["Ratio combinado %"].idxmax()
    texto = (f"Acumulado a {MESES[mes - 1]}: primas devengadas {tot['Primas devengadas'] / 1e6:,.1f} M€, "
             f"margen técnico {tot['Margen técnico'] / 1e6:,.2f} M€ (ratio combinado "
             f"{tot['Ratio combinado %']:.1%}). Desviación del margen frente a presupuesto: "
             f"{desv_margen / 1e6:+,.2f} M€. Canal con peor ratio combinado: {peor} "
             f"({t.loc[peor, 'Ratio combinado %']:.1%}).")
    pdf.multi_cell(0, 5, texto)
    pdf.ln(3)

    cols = ["Primas devengadas", "Coste de siniestros", "Margen técnico", "Siniestralidad %",
            "Ratio combinado %"]
    cab = ["Canal", "Primas (k€)", "Siniestros (k€)", "Margen (k€)", "Siniestr.", "R. combinado"]
    anchos = [34, 32, 32, 32, 28, 30]
    with pdf.table(col_widths=anchos, text_align=("LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"),
                   line_height=6, first_row_as_headings=True) as tabla:
        fila = tabla.row()
        for c in cab:
            fila.cell(c)
        for canal, r in t.iterrows():
            fila = tabla.row()
            fila.cell(str(canal))
            for c in cols:
                v = r[c]
                fila.cell(f"{v:.1%}" if "%" in c else f"{v / 1e3:,.0f}".replace(",", "."))
    pdf.ln(4)
    png = grafico_margen(res, ruta.with_suffix(".png"))
    pdf.image(str(png), w=180)
    pdf.ln(2)
    c = res["controles"]
    n_ko = (c["resultado"] == "KO").sum()
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 7, f"Controles de calidad: {len(c)} ejecutados · {n_ko} KO · "
                   f"{(c['resultado'] == 'AVISO').sum()} avisos", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 8)
    for _, r in c[c["resultado"] != "OK"].sort_values("mes", ascending=False).head(12).iterrows():
        pdf.cell(0, 4.5, f"[{r['resultado']}] mes {r['mes']} · {r['control']} · {r['detalle']}",
                 new_x="LMARGIN", new_y="NEXT")
    pdf.output(str(ruta))
    png.unlink(missing_ok=True)
    return ruta
