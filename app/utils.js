import { PythonShell } from "python-shell";
import { join } from "path";

export const pyConnections = {
  insertIntoDb: (message, sender, exp = "") => {
    const pyShell = createPythonCon("dataBaseConnection", "json");
    if (exp === "initial") {
      pyShell.send(createData("", "", exp));
    } else {
      pyShell.send(createData(message, sender, exp));
    }
    pyShell.on("message", message => {
      console.log(message);
    });

    //   end the input stream and allow the process to exit
    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log(
        `Python File dataBaseConnection.py ended with code: ${code} and signal: ${signal}`
      );
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
        console.log(response);
      } else if (exp === "entry") {
        setstateFunc([...state, response[0]]);
        console.log([...state, ...response]);
        console.log(...response);
      } else if (exp === "loadMore") {
        setstateFunc([...response, ...state]);
      } else {
        console.error("queue is not defined!!" + exp);
      }
    });

    //   end the input stream and allow the process to exit
    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log(
        `Python File getFromDb.py ended with code: ${code} and signal: ${signal}`
      );
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

const createData = (message, sender, exp) => {
  return {
    message: message,
    sender: sender,
    load: exp
  };
};
