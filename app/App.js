"use babel";

import React, { useState, useEffect } from "react";
import { PythonShell } from "python-shell";
import { Paper, Grid, Container, Box } from "@material-ui/core";
import { ThemeProvider } from "@material-ui/styles";
import { ChatInput } from "./ChatInput";
import { ChatWindow } from "./ChatWindow";
import { createMuiTheme } from "@material-ui/core/styles";

const darkTheme = createMuiTheme({
  palette: {
    type: "dark"
  }
});

const App = () => {
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
    // <ThemeProvider theme="">
    <Box>
      <ChatWindow />
      <ChatInput />
      <Box>{msg}</Box>
    </Box>
    // </ThemeProvider>
  );
};
export default App;
