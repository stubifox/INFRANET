import { app, BrowserWindow } from "electron";
import { createPythonCon, pyConnections } from "./app/helpers/pyConnections";
import { Action } from "./app/helpers/shared";
let mainWindow = null;
let pyListener = createPythonCon("PyToSerMain", "text");

app.on("window-all-closed", () => {
  if (process.platform != "darwin") {
    pyListener.terminate();
    app.quit();
  }
});

app.on("ready", () => {
  mainWindow = new BrowserWindow({
    webPreferences: {
      nodeIntegration: true
    },
    width: 800,
    height: 600
  });
  mainWindow.loadURL("file://" + __dirname + "/index.html");
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
});
