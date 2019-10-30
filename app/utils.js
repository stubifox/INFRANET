import { PythonShell } from "python-shell";
import { join } from "path";

export const pyConnections = {
  insertIntoDb: async (message, sender) => {
    const pyShell = createPythonCon("dataBaseConnection", "json");
    pyShell.send(createData(message, sender));
    await pyShell.on("message", message => {
      console.log(message);
    });

    //   end the input stream and allow the process to exit
    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log("The exit code was: " + code);
      console.log("The exit signal was: " + signal);
      console.log("finished");
    });
    return;
  },

  getFromDb: async (exp, setstateFunc, state) => {
    const pyShell = createPythonCon("getFromDb", "json");
    if (exp === "loadMore") {
      pyShell.send({ load: exp, id: state[0].id });
    } else {
      pyShell.send({ load: exp });
    }
    await pyShell.on("message", response => {
      if (exp === "initial") {
        setstateFunc(response);
      } else if (exp === "entry") {
        setstateFunc([...state, response[0]]);
      } else if (exp === "loadMore") {
        setstateFunc([...response, ...state]);
      } else {
        console.error("queue is not defined!!" + exp);
      }
    });

    //   end the input stream and allow the process to exit
    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log("The exit code was: " + code);
      console.log("The exit signal was: " + signal);
      console.log("finished");
    });
    return;
  }
};
/**
 *
 * @param {String} fileName Python file in ./app folder!! without .py!!
 * @param {['json', 'text']} mode specifies the mode the data is send to Python
 */
const createPythonCon = (fileName, mode) => {
  return new PythonShell(join(__dirname, "communicate", `${fileName}.py`), {
    mode: mode
  });
};

const createData = (message, sender) => {
  return {
    message: message,
    sender: sender
  };
};
