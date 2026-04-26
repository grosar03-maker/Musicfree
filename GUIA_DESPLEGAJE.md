# 🎵 Musicfree - Guía de Despliegue a Render

## Requisitos previos
- Cuenta en GitHub (github.com)
- Cuenta en Render (render.com)

---

## Paso 1: Subir el proyecto a GitHub

### 1.1 Ve a GitHub y crea un nuevo repositorio
1. Abre **github.com** e inicia sesión
2. Click en **"+"** (arriba derecha) → **"New repository"**
3. En **"Repository name"** escribe: `Musicfree`
4. Elige **"Public"**
5. Desmarca las casillas de README
6. Click **"Create repository"**

### 1.2 Sube los archivos
En tu PC, abre la terminal (PowerShell o CMD) y Ejecuta:

```bash
cd "C:\Users\grosa\OneDrive\Escritorio\MusicFinder-main"
```

Luego estos comandos (uno por uno):

```bash
git init
git add .
git commit -m "primera version"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/Musicfree.git
git push -u origin main
```

*(Cambia "TU_USUARIO" por tu nombre de usuario de GitHub)*

---

## Paso 2: Crear el servicio en Render

### 2.1 Entra a Render
1. Ve a **dashboard.render.com**
2. Inicia sesión con tu cuenta de GitHub
3. Click **"New +"** (arriba azul)
4. Click **"Web Service"**

### 2.2 Conecta GitHub
1. En **"Connect a repository"**, busca `Musicfree`
2. Click en el cuando aparezca
3. Click **"Connect"**

### 2.3 Configura el servicio
En la página de configuración:

| Campo | Valor |
|------|-------|
| **Name** | `musicgosth` |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind=0.0.0.0:$PORT` |
| **Plan** | `Free` |

### 2.4 Despliega
1. Baja al final de la página
2. Click **"Create Web Service"** (azul)

### 2.5 Espera
- Verás logs en pantalla
- Espera 2-3 minutos
- Cuando diga **"Deploy complete"** estás listo

---

## Paso 3: Usar la app

### 3.1 Obtener el enlace
1. En Render, busca la URL (arriba del deploy)
2. Será algo como: `https://musicgosth.onrender.com`
3. ¡Eso es lo que le das a tu familia!

### 3.2 Compartir
- Envía el enlace a tu familia por WhatsApp
- Ya pueden usarlo desde cualquier dispositivo

---

## Notas importantes

- **Gratuituitud**: El plan Free de Render es gratis
- **Límites**: Se duerme después de 15 min sin usar
- **Wake**: Cuando alguien lo use, despierta en ~30 seg
- **Ancho de banda**: 750 GB/mes (mucho para familia)

---

## Si algo falla

### Error de Build
Revisa que subiste todos los archivos:
- `app.py`
- `templates/index.html`
- `requirements.txt`
- `Procfile`

### Error 500 al buscar
- Es normal al inicio
- Retry 2-3 veces
- YouTube a veces bloquea IPs de Render

### No encuentra la página
- Espera 5 min después del deploy
- Revisa el URL en Render dashboard