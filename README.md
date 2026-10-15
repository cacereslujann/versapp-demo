# Versapp Demo — app Android de prueba

App nativa Java: muestra version, numero de build, entorno y un contador con reinicio. No necesita Internet ni permisos especiales. Android 6 o superior. Genera un APK **debug**, para pruebas, no una publicacion de produccion.

## 1. Subir a GitHub y obtener el primer APK

1. Crea un repositorio llamado `versapp-demo` en tu cuenta de GitHub, inicialmente sin README ni otros archivos.
2. Extrae este proyecto. Abre su carpeta en VS Code y ejecuta:

```powershell
git init -b main
git add .
git commit -m "Crear app Android de prueba para Versapp"
git remote add origin https://github.com/TU_USUARIO/versapp-demo.git
git push -u origin main
```

Reemplaza TU_USUARIO por el usuario de tu cuenta; no por el correo. Conserva `.github/workflows/build-apk.yml` en el repositorio (es una carpeta oculta).

3. En GitHub abre **Actions → Versapp Demo APK**. El primer push a main compila sin configurar secretos de Versapp.
4. Cuando termine, descarga `versapp-demo-apk-N` en **Artifacts**, extrae el ZIP y usa `app-debug.apk` para una carga manual en Versapp o para instalarlo en un dispositivo de prueba. Inicia sesion en GitHub para descargar el artefacto.

## 2. Usarlo desde Automatizado de Versapp

En Proyectos de Versapp, edita `documentacion-app`:

- GitHub Repo: `TU_USUARIO/versapp-demo`.
- Configura un token de GitHub autorizado para leer ese repositorio y ejecutar Actions. Este token es distinto del de Jira y de la API key del proyecto Versapp.
- Workflow: `build-apk.yml`.
- Rama: `main`. En DEV (local), configura tambien tu rama personal `main` y el workflow si la pantalla lo requiere.

El workflow debe estar en la rama principal para que GitHub permita `workflow_dispatch`. Acepta exactamente los inputs que envia el backend actual: `version`, `entorno`, `build_numero`, `build_id`.

## 3. Permitir que GitHub entregue el APK a Versapp

En GitHub → Settings → Secrets and variables → Actions → New repository secret:

| Secret | Valor |
| --- | --- |
| VERSAPP_URL | URL HTTPS publica de tu servidor Versapp, sin `/api` al final |
| VERSAPP_API_KEY | API key del proyecto `documentacion-app`, obtenida en Versapp |

**No uses `http://localhost:3000` como VERSAPP_URL**: el workflow corre en GitHub, en otra computadora. Para probar con tu PC necesitas un tunel HTTPS hacia el puerto 3000, o un servidor desplegado. El tunel debe permanecer funcionando durante la build y la entrega. No se ha configurado ningun tunel ni despliegue en este proyecto.

Cuando inicies una build desde Versapp, el backend crea la fila pendiente y envia su `build_id`. El workflow compila, guarda el artefacto y envia el APK por `POST /api/versiones/upload` con `x-api-key` y el mismo `build_id`; asi completa la fila existente y conserva los tickets seleccionados. No hace falta configurar un webhook GitHub adicional para este flujo.

Si ejecutas el workflow desde GitHub con `build_id` vacio, solo genera el artefacto: no crea versiones en Versapp. No inventes un ID para evitar asociar el APK a una build incorrecta.

## 4. Verificacion de la prueba

1. Selecciona proyecto, version (por ejemplo `1.0.1`), entorno y tickets del sprint en Versapp.
2. Ejecuta la build automatizada. Revisa Actions si falla.
3. Comprueba que el historial pasa de Pendiente a Completado y ofrece descarga.
4. Instala el APK y compara version, build y entorno con el registro.
5. Pulsa el contador y reinicialo; al girar el dispositivo debe conservarse su valor.

Si falla la compilacion o la entrega, el APK puede no llegar y la fila de Versapp puede quedar pendiente. Este ejemplo no envia una notificacion automatica de fallo; revisa el log de Actions antes de reintentar. En un reintento no vuelvas a enviar un APK a una build ya completada.

## 5. Herramientas y limites

GitHub instala JDK 17, SDK 35 y Gradle 8.11.1; el proyecto usa Android Gradle Plugin 8.9.2. No incluye Gradle Wrapper: el workflow instala una version fija de Gradle. Para compilar localmente necesitas esas herramientas y ejecutar `gradle :app:assembleDebug`, o abrir el proyecto en Android Studio y configurar Gradle local.

Se verifico la estructura y compatibilidad con los endpoints del codigo local de Versapp. La compilacion Android y la entrega real deben confirmarse en GitHub Actions; este paquete no contiene un APK precompilado ni credenciales. Los dos secrets solo son necesarios para la entrega automatica.

Referencias: [AGP 8.9 y compatibilidad](https://developer.android.com/build/releases/agp-8-9-0-release-notes), [instalar Gradle en GitHub Actions](https://github.com/gradle/actions/blob/main/docs/setup-gradle.md).
