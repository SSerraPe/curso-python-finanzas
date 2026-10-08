"""Construcción de correos con adjuntos.

Por defecto trabajamos en MODO SIMULACRO: los correos se guardan como ficheros
.eml (se abren con doble clic en Outlook) en lugar de enviarse. Así se puede
revisar todo antes de activar el envío real.

Envío real en una empresa: lo habitual es Microsoft Graph (Office 365) u
Outlook vía `win32com` en Windows, configurado con IT. El envío SMTP con
usuario/contraseña está siendo retirado en Exchange Online.
"""
from __future__ import annotations

import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path


def construir_correo(remitente: str, destinatarios: list[str] | str, asunto: str, cuerpo: str,
                     adjuntos: list[Path] | None = None, cuerpo_html: str | None = None) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = remitente
    msg["To"] = destinatarios if isinstance(destinatarios, str) else ", ".join(destinatarios)
    msg["Subject"] = asunto
    msg.set_content(cuerpo)
    if cuerpo_html:
        msg.add_alternative(cuerpo_html, subtype="html")
    for ruta in adjuntos or []:
        ruta = Path(ruta)
        tipo, _ = mimetypes.guess_type(ruta.name)
        principal, sub = (tipo or "application/octet-stream").split("/", 1)
        msg.add_attachment(ruta.read_bytes(), maintype=principal, subtype=sub, filename=ruta.name)
    return msg


def guardar_eml(msg: EmailMessage, carpeta: Path, nombre: str) -> Path:
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"{nombre}.eml"
    ruta.write_bytes(bytes(msg))
    return ruta


def enviar_smtp(msg: EmailMessage, servidor: str, puerto: int = 587, usuario: str | None = None,
                clave: str | None = None) -> None:
    """Envío real por SMTP (NO usar en clase). Las credenciales nunca en el código:
    léelas de variables de entorno o de un gestor de secretos."""
    with smtplib.SMTP(servidor, puerto) as s:
        s.starttls()
        if usuario:
            s.login(usuario, clave or "")
        s.send_message(msg)
