"use babel";

import React from "react";
import PythonShell from "python-shell";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import Chat from "./Chat";

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      msg: "loading..." || []
    };
  }

  componentDidMount() {
    let options = {
      mode: "text",
      pythonPath: "venv/bin/python",
      pythonOptions: ["-u"],
      scriptPath: "app/",
      args: ["value1", 10]
    };
    PythonShell.run("worker.py", options, (err, results) => {
      if (err) {
        console.error("Got error: ", err);
      } else {
        this.setState({ msg: results });
        console.log(results[1]);
      }
    });
  }

  render() {
    return (
      <div>
        <MuiThemeProvider>
          <Chat />
        </MuiThemeProvider>
        <div>{this.state.msg}</div>
      </div>
    );
  }
}
