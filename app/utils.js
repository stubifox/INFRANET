import { PythonShell } from "python-shell";
import { join } from "path";

export const pyConnections = {
  insertIntoDb: (message, sender) => {
    const pyShell = createPythonCon("dataBaseConnection", "json");
    pyShell.send(createData(message, sender));
    pyShell.on("message", message => {
      console.log(message);
    });

    //   end the input stream and allow the process to exit
    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log("The exit code was: " + code);
      console.log("The exit signal was: " + signal);
      console.log("finished");
    });
  },

  getFromDb: (exp, setstateFunc) => {
    const pyShell = createPythonCon("getFromDb", "json");
    pyShell.send({ test: 1 });
    console.log(exp);
    pyShell.on("message", response => {
      setstateFunc(response);
    });

    //   end the input stream and allow the process to exit
    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log("The exit code was: " + code);
      console.log("The exit signal was: " + signal);
      console.log("finished");
    });
  }
};
/**
 *
 * @param {String} fileName Python file in ./app folder!! without .py!!
 * @param {['json', 'text']} mode specifies the mode the data is send to Python
 */
const createPythonCon = (fileName, mode = "text") => {
  return new PythonShell(join(__dirname, `${fileName}.py`), {
    mode: mode
  });
};

const createData = (message, sender) => {
  return {
    message: message,
    sender: sender
  };
};
