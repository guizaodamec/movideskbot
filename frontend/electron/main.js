const { app, BrowserWindow, ipcMain, globalShortcut } = require('electron')
const path = require('path')
const { spawn } = require('child_process')
const http = require('http')
const fs = require('fs')

const isDev = !app.isPackaged

let mainWindow = null
let backendProcess = null

// ── Janela principal ───────────────────────────────────────────────────────────

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    frame: false,
    backgroundColor: '#0f1117',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    show: false,
  })

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    // mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
    const bounds = mainWindow.getBounds()
    const screen = require('electron').screen.getPrimaryDisplay().workAreaSize
    if (bounds.width >= screen.width || bounds.height >= screen.height) {
      mainWindow.maximize()
    }
  })

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// ── Backend Python ────────────────────────────────────────────────────────────

function startBackend() {
  if (isDev) return // Em dev, rodar o backend manualmente

  // Tenta primeiro o backend compilado (backend.exe) — portátil, sem Python
  const backendExe = path.join(process.resourcesPath, 'backend.exe')
  if (fs.existsSync(backendExe)) {
    backendProcess = spawn(backendExe, [], {
      cwd: process.resourcesPath,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: Object.assign({}, process.env),
    })
    backendProcess.stdout.on('data', d => console.log('[backend]', d.toString().trim()))
    backendProcess.stderr.on('data', d => console.error('[backend err]', d.toString().trim()))
    backendProcess.on('exit', code => console.log('[backend] saiu com código', code))
    return
  }

  // Fallback: Python instalado na máquina
  const backendDir = path.join(process.resourcesPath, 'backend')
  const scriptPath = path.join(backendDir, 'main.py')

  const candidates = ['python3', 'python', path.join(backendDir, 'python', 'python.exe')]
  const python = candidates.find(p => {
    try {
      require('child_process').execSync('"' + p + '" --version', { stdio: 'ignore' })
      return true
    } catch {
      return false
    }
  }) || 'python'

  backendProcess = spawn(python, [scriptPath], {
    cwd: backendDir,
    stdio: ['ignore', 'pipe', 'pipe'],
    env: Object.assign({}, process.env),
  })

  backendProcess.stdout.on('data', d => console.log('[backend]', d.toString().trim()))
  backendProcess.stderr.on('data', d => console.error('[backend err]', d.toString().trim()))
  backendProcess.on('exit', code => console.log('[backend] saiu com código', code))
}

function waitForBackend(maxTries, intervalMs) {
  return new Promise(function (resolve, reject) {
    var tries = 0
    function attempt() {
      tries++
      var req = http.get('http://localhost:5000/api/health', function (res) {
        res.resume()
        if (res.statusCode === 200) return resolve()
        retry()
      })
      req.on('error', retry)
      req.setTimeout(400, function () { req.destroy(); retry() })
    }
    function retry() {
      if (tries >= maxTries) return reject(new Error('Backend não respondeu em ' + (maxTries * intervalMs / 1000) + 's'))
      setTimeout(attempt, intervalMs)
    }
    attempt()
  })
}

// ── IPC ────────────────────────────────────────────────────────────────────────

ipcMain.on('window-minimize', function () { mainWindow && mainWindow.minimize() })
ipcMain.on('window-maximize', function () {
  if (!mainWindow) return
  mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize()
})
ipcMain.on('window-close', function () { mainWindow && mainWindow.close() })
ipcMain.handle('window-is-maximized', function () {
  return mainWindow ? mainWindow.isMaximized() : false
})

// ── App lifecycle ──────────────────────────────────────────────────────────────

app.whenReady().then(function () {
  startBackend()
  createWindow()

  if (isDev) {
    // Em dev notifica imediatamente (backend deve estar rodando manualmente)
    setTimeout(function () {
      if (mainWindow) mainWindow.webContents.send('backend-ready')
    }, 800)
  } else {
    waitForBackend(20, 500)
      .then(function () {
        if (mainWindow) mainWindow.webContents.send('backend-ready')
      })
      .catch(function (err) {
        if (mainWindow) mainWindow.webContents.send('backend-error', err.message)
      })
  }

  // Atalho global Ctrl+Shift+P
  globalShortcut.register('CommandOrControl+Shift+P', function () {
    if (mainWindow) mainWindow.webContents.send('capture-shortcut')
  })

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', function () {
  globalShortcut.unregisterAll()
  if (backendProcess) backendProcess.kill()
  if (process.platform !== 'darwin') app.quit()
})

app.on('will-quit', function () {
  globalShortcut.unregisterAll()
  if (backendProcess) backendProcess.kill()
})
