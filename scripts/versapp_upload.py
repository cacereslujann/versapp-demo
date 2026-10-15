"""Envia un APK a la build pendiente creada por Versapp; usa solo la biblioteca estandar."""
import os
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse
import uuid
import sys


def main():
    base = os.environ.get('VERSAPP_URL', '').strip().rstrip('/')
    key = os.environ.get('VERSAPP_API_KEY', '').strip()
    build_id = os.environ.get('BUILD_ID', '').strip()
    parsed = urllib.parse.urlparse(base)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Configura VERSAPP_URL con una URL HTTPS publica, sin credenciales ni parametros.')
    if parsed.hostname in ('localhost', '127.0.0.1', '::1'):
        raise ValueError('GitHub no puede conectarse al localhost de tu PC. Usa una URL publica HTTPS.')
    if not key or not build_id.isdigit() or int(build_id) < 1:
        raise ValueError('Falta VERSAPP_API_KEY o el build_id valido enviado por Versapp.')
    apk = Path('app/build/outputs/apk/debug/app-debug.apk')
    if not apk.is_file():
        raise ValueError('No se encontro el APK compilado.')
    boundary = 'Versapp' + uuid.uuid4().hex
    fields = {'build_id': build_id, 'version': os.environ.get('DEMO_VERSION', '1.0.0'),
              'entorno': os.environ.get('DEMO_ENVIRONMENT', 'dev')}
    data = bytearray()
    for name, value in fields.items():
        data.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    data.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="apk"; filename="app-debug.apk"\r\nContent-Type: application/vnd.android.package-archive\r\n\r\n'.encode())
    data.extend(apk.read_bytes())
    data.extend(f'\r\n--{boundary}--\r\n'.encode())
    request = urllib.request.Request(base + '/api/versiones/upload', data=bytes(data), method='POST',
        headers={'x-api-key': key, 'Content-Type': 'multipart/form-data; boundary=' + boundary})
    # No seguir redirecciones: evita reenviar la API key a otro destino.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=120) as response:
            print('APK enviado a Versapp. HTTP', response.status)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f'Versapp respondio HTTP {error.code}. Revisa el servidor y la API key; el APK queda disponible en Artifacts.') from None
    except urllib.error.URLError:
        raise RuntimeError('No se pudo conectar con Versapp. Revisa la URL publica y que el servidor este funcionando.') from None


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
