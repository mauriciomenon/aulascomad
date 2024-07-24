const { app, BrowserWindow, ipcMain, clipboard } = require('electron');
const path = require('path');
const axios = require('axios');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: false,
      nodeIntegration: true,
    },
  });

  mainWindow.loadFile('index.html');
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.handle('shorten-url', async (event, url) => {
  try {
    const response = await axios.post('https://api.tinyurl.com/create', {
      url,
      domain: 'tiny.one',
      alias: '',
    }, {
      headers: {
        Authorization: 'Bearer YOUR_API_KEY',  // Substitua 'YOUR_API_KEY' pela sua chave de API
        'Content-Type': 'application/json'
      }
    });
    return response.data.data.tiny_url;
  } catch (error) {
    console.error(error);
    return `Error: ${error.message}`;
  }
});

ipcMain.handle('copy-to-clipboard', (event, text) => {
  clipboard.writeText(text);
});
