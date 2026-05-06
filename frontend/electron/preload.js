const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electron', {
  minimize:    () => ipcRenderer.send('window-minimize'),
  maximize:    () => ipcRenderer.send('window-maximize'),
  close:       () => ipcRenderer.send('window-close'),
  isMaximized: () => ipcRenderer.invoke('window-is-maximized'),

  onBackendReady:    (cb) => ipcRenderer.on('backend-ready', cb),
  onBackendError:    (cb) => ipcRenderer.on('backend-error', (_, msg) => cb(msg)),
  onCaptureShortcut: (cb) => ipcRenderer.on('capture-shortcut', cb),

  removeListener: (channel) => ipcRenderer.removeAllListeners(channel),
})
