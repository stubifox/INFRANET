/**
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:49:36
 * @modify date 2019-11-28 22:49:36
 * @desc [description]
 */

import { PythonShell } from "python-shell";
import { join } from "path";
import {
  createData,
  createDefaultsData,
  createReceivingData
} from "./createDataObjects";
//import uuidv1 from "uuid";
import { Action, printLoggingOrErrorMessages } from "./shared";

/**
 * Object holding different Functions to communicate with Python Scripts.
 *
 * States are being updated depending on returning message of the Scripts.
 *
 * Communication realized via Stdin and Stdout.
 *
 * Protocol for communication is JSON.
 */
export const pyConnections = {
  /**
   * @param {Action} exp an expression telling the func what to do, NOT REQUIRED!
   * @param {string} message the  message to insert into the db
   * @param {string} sender the sender to insert into the db
   */

  insertIntoDb: async (message, sender, exp = "") => {
    const pyShell = createPythonCon("dataBaseConnection", "json");

    if (exp === Action.INITIAL) {
      pyShell.send(createData("", "", exp));
    } else if (exp === Action.INSERT) {
      pyShell.send(createData(message, sender, exp));
    }

    pyShell.on("message", message => {
      printLoggingOrErrorMessages(message);
    });

    await pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log(
        `Python File dataBaseConnection.py ended with code: ${code} and signal: ${signal}`
      );
    });
    return;
  },

  /**
   * @param {Action} exp an expression to say the func what to do
   * @param {'function'} setmessages a state Function to update the state
   * @param {'React.state'} messages the corresponding state to the state Function
   */

  getFromDb: (exp, setmessages, messages) => {
    const pyShell = createPythonCon("getFromDb", "json");
    if (exp === Action.LOAD_MORE) {
      pyShell.send(createReceivingData(exp, messages[0].id));
    } else {
      pyShell.send(createReceivingData(exp, ""));
    }

    pyShell.on("message", response => {
      printLoggingOrErrorMessages(response);

      if (exp === Action.INITIAL) {
        setmessages(response);
      } else if (exp === Action.ENTRY) {
        return;
      } else if (exp === Action.LOAD_MORE) {
        setmessages([...response, ...messages]);
      } else {
        console.error("queue is not defined!!" + exp);
      }
    });

    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log(
        `Python File getFromDb.py ended with code: ${code} and signal: ${signal}`
      );
    });
    return;
  },

  /**
   * @param {'destructured State'} obj the corresponding state to the stateFunc. will be destructured inside the Function.
   * @param {'React.state'} setuserDefaults the function to update the State
   * @param {Action} exp an expression to say the func what to do
   */

  userDefaultsHandler: ({ userTheme }, setuserDefaults, exp) => {
    const pyShell = createPythonCon("userDefaultsHandler", "json");

    /**
     * checking if user has already default Data stored in the DB.
     * if so Python File will return the data.
     */
    if (exp === Action.INITIAL) {
      pyShell.send(createDefaultsData(userTheme, Action.CHECK));
    }

    if (exp === Action.UPDATE_THEME) {
      pyShell.send(createDefaultsData(userTheme, exp));
    }

    pyShell.on("message", message => {
      printLoggingOrErrorMessages(message);

      if (exp === Action.INITIAL) {
        setuserDefaults({
          sender: message[0].value,
          userTheme: message[1].value === "True"
        });
      }
    });

    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log(
        `Python File userDefaultsHandler.py ended with code: ${code} and signal: ${signal}`
      );
    });
  },

  getExternalStateChanges: (
    { internalArduinoConnected, externalArduinoConnected, chatPartnerUUID },
    setExternalStates,
    messages,
    setmessages
  ) => {
    const pyShell = createPythonCon("updateExternalStates", "json");
    if (messages.length > 0) {
      const lastID = messages.slice(-1).pop().id;
      pyShell.send(createReceivingData(Action.ID, lastID));
    } else {
      pyShell.send(createReceivingData(Action.INITIAL, undefined));
    }
    pyShell.on("message", updates => {
      printLoggingOrErrorMessages(updates);

      if (updates[Action.SHOULD_UPDATE_MESSAGES]) {
        setmessages([...messages, ...updates[Action.NEW_MESSAGES]]);
      } else {
        setExternalStates({
          internalArduinoConnected:
            updates[Action.LOCAL_ARDUINO_STATE] === "True",
          externalArduinoConnected:
            updates[Action.EXTERNAL_ARDUINO_STATE] === "True",
          chatPartnerUUID: updates[Action.PARTNER_ID]
        });
      }
    });

    pyShell.end((err, code, signal) => {
      if (err) throw err;
    });
  }
};

/**
 * @param {String} fileName Python file in ./app/communicate folder!! without .py!!
 * @param {['json', 'text']} mode specifies the mode the data is send to Python
 * @returns {'PythonShell'} pyShell returns a Python Shell instance
 */
export const createPythonCon = (fileName, mode) => {
  return new PythonShell(
    join(__dirname, "..", "communicate", `${fileName}.py`),
    {
      mode: mode
    }
  );
};
