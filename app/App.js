"use babel";

import React, { useState, useEffect } from "react";
import { PythonShell } from "python-shell";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import Chat from "./Chat";

const App = props => {
  const [msg, setmsg] = useState("loading...");

  useEffect(() => {
    const platform = navigator.platform;
    let options = {
      mode: "text",
      pythonPath: platform.includes("Win")
        ? "venv/Scripts/python"
        : "venv/bin/python",
      pythonOptions: ["-u"],
      scriptPath: "app/",
      args: ["value1", 10]
    };
    PythonShell.run("worker.py", options, (err, results) => {
      if (err) {
        console.error("Got error: ", err);
      } else {
        setmsg(results);
        console.log(results[1]);
      }
    });
  }, []);

  return (
    <div>
      <MuiThemeProvider>
        <Chat />
      </MuiThemeProvider>
      <div>{msg}</div>
    </div>
  );
};
export default App;
