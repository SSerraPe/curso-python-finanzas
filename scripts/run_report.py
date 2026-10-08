"""
Cierre mensual automático del ramo Autos.

Ejecuta, en un solo paso:
  1. Carga y valida los bordereaux de siniestros hasta el mes indicado.
  2. Calcula la cuenta técnica real (primas, siniestros, comisiones, gastos).
  3. Compara contra presupuesto (mes y acumulado).
  4. Genera Excel completo + un Excel por canal + PDF resumen.
  5. Prepara un correo por responsable de canal (simulacro: ficheros .eml).

Uso:
    python scripts/run_report.py                    # usa el periodo de config/params.yaml
    python scripts/run_report.py --periodo 2025-06
    python scripts/run_report.py --periodo 2025-12 --sin-correos

Programarlo (Windows):  Programador de tareas → Crear tarea básica → Acción
"Iniciar un programa" → python.exe con argumentos "scripts\\run_report.py".
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from curso_seguros.cierre import ejecutar_cierre  # noqa: E402
from curso_seguros.correo import construir_correo, guardar_eml  # noqa: E402
from curso_seguros.informes import MESES, escribir_excel_cierre, generar_pdf_cierre  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    cfg = yaml.safe_load((RAIZ / "config" / "params.yaml").read_text(encoding="utf-8"))
    ap = argparse.ArgumentParser(description="Cierre mensual automático")
    ap.add_argument("--periodo", default=cfg["periodo"], help="AAAA-MM")
    ap.add_argument("--sin-correos", action="store_true")
    args = ap.parse_args(argv)

    salida = RAIZ / cfg["salidas"]["carpeta"] / args.periodo
    salida.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                        handlers=[logging.StreamHandler(),
                                  logging.FileHandler(salida / "ejecucion.log", encoding="utf-8")])
    logging.getLogger("fontTools").setLevel(logging.WARNING)
    log = logging.getLogger("run_report")

    mes = int(args.periodo[-2:])
    log.info("=== Cierre %s ===", args.periodo)
    res = ejecutar_cierre(mes)

    n_ko = int((res["controles"]["resultado"] == "KO").sum())
    log.info("Controles: %d KO de %d", n_ko, len(res["controles"]))
    if n_ko and cfg["controles"]["detener_si_ko"]:
        log.error("Hay controles KO y detener_si_ko=true. No se generan informes.")
        return 1

    ficheros = {}
    if cfg["salidas"]["excel"]:
        ficheros["excel"] = escribir_excel_cierre(res, salida / f"cierre_{args.periodo}.xlsx")
        for canal in cfg["correo"]["destinatarios"]:
            ficheros[canal] = escribir_excel_cierre(res, salida / "por_canal" / f"cierre_{args.periodo}_{canal}.xlsx",
                                                    canal=canal)
        log.info("Excel generados en %s", salida)
    if cfg["salidas"]["pdf"]:
        ficheros["pdf"] = generar_pdf_cierre(res, salida / f"cierre_{args.periodo}.pdf")
        log.info("PDF generado: %s", ficheros["pdf"].name)

    if cfg["salidas"]["correos"] and not args.sin_correos:
        t = res["resultado_ytd"]
        for canal, destinatarios in cfg["correo"]["destinatarios"].items():
            r = t.loc[canal]
            cuerpo = (f"Hola,\n\nTe adjunto el cierre de {MESES[mes - 1]} 2025 del canal {canal}.\n\n"
                      f"Acumulado del año:\n"
                      f"  · Primas devengadas: {r['Primas devengadas']:,.0f} €\n"
                      f"  · Margen técnico:    {r['Margen técnico']:,.0f} €\n"
                      f"  · Ratio combinado:   {r['Ratio combinado %']:.1%}\n\n"
                      f"Cualquier duda, quedamos a tu disposición.\n\nEquipo FP&A Autos")
            msg = construir_correo(cfg["correo"]["remitente"], destinatarios + cfg["correo"]["copia_direccion"],
                                   f"Cierre {args.periodo} · Canal {canal}", cuerpo,
                                   adjuntos=[ficheros[canal], ficheros.get("pdf")] if "pdf" in ficheros
                                   else [ficheros[canal]])
            if cfg["correo"]["modo_simulacro"]:
                ruta = guardar_eml(msg, salida / "correos", f"correo_{canal}")
                log.info("Correo (simulacro) guardado: %s", ruta.name)
            else:
                log.warning("Envío real no configurado en este curso. Consulta con IT (Microsoft Graph).")
    log.info("=== Fin del cierre %s ===", args.periodo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
