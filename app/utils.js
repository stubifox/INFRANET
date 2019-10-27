import { PythonShell } from "python-shell";
import { join } from "path";

export const sendTextToPython = message => {
  const pyShell = new PythonShell(join(__dirname, "worker.py"), {
    mode: "json"
  });
  pyShell.send(createData(message));
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
};

export const getTime = () => {
  const today = new Date();
  const time = today.getHours() + ":" + today.getMinutes();
  return time;
};

export const getDate = () => {
  const today = new Date();
  const date =
    today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
  return date;
};

export const createData = message => {
  return {
    time: getTime(),
    date: getDate(),
    message: message,
    sender: "max"
  };
};
