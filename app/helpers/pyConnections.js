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
import uuidv1 from "uuid";
import { Action } from "./shared";

/**
 * Object holding different Functions to communicate with Python Scripts.
 *
 * states are being updated depending on returning message of the Scripts.
 *
 * Communication realized via Stdin and Stdout.
 * protocol for communication is JSON.
 */
export const pyConnections = {
  /**
   * @param {['initial', '']} exp an expression telling the func what to do, NOT REQUIRED!
   * @param {string} message the  message to insert into the db
   * @param {string} sender the sender to insert into the db
   */

  insertIntoDb: (message, sender, exp = "") => {
    const pyShell = createPythonCon("dataBaseConnection", "json");
    /**
     * on initial App load just check if DB is existent.
     */

    if (exp === Action.INITIAL) {
      pyShell.send(createData("", "", exp));
    } else if (exp === Action.INSERT) {
      console.log("insert");
      /**
       * normal message input received. store message and sender into DB.
       */
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

  /**
   * @param {['loadMore', 'initial', 'entry']} exp an expression to say the func what to do
   * @param {'function'} setmessages a state Function to update the state
   * @param {'React.state'} messages the corresponding state to the state Function
   */

  getFromDb: async (exp, setmessages, messages) => {
    console.log(exp);
    const pyShell = createPythonCon("getFromDb", "json");

    /**
     * load more entries out of DB starting with id at index 0 of current message Array.
     */
    if (exp === Action.LOAD_MORE) {
      // pyShell.send({ load: exp, id: messages[0].id, receiver: receiver });
      pyShell.send(createReceivingData(exp, messages[0].id));
    } else {
      /**
       * load last 20 messages out of DB.
       */
      pyShell.send(createReceivingData(exp, ""));
    }

    await pyShell.on("message", response => {
      console.log(response);
      /**
       * initial load: message-Array is just filled with whole response (20 messages)
       */
      if (exp === Action.INITIAL) {
        setmessages(response);

        /**
         * getting the last inserted Message out of DB.
         * happens when user inputs a message.
         */
      } else if (exp === Action.ENTRY) {
        setmessages([...messages, response[0]]);
        /**
         * user wants to load more messages starting from top.
         * will be appended in front of current state.
         */
      } else if (exp === Action.LOAD_MORE) {
        setmessages([...response, ...messages]);
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
  },

  /**
   * @param {'destructured State'} obj the corresponding state to the stateFunc. will be destructured inside the Function.
   * @param {'React.state'} setuserDefaults the function to update the State
   * @param {['initial', 'insertUUID', 'updateTheme']} exp an expression to say the func what to do
   */

  userDefaultsHandler: ({ sender, userTheme }, setuserDefaults, exp) => {
    const pyShell = createPythonCon("userDefaultsHandler", "json");

    /**
     * checking if user has already default Data stored in the DB.
     * if so Python File will return the data.
     */
    if (exp === Action.INITIAL) {
      pyShell.send(createDefaultsData("", "", Action.CHECK));
    }

    /**
     * if no data is deposited, insert Data into DB
     * also create a UUID for identification purposes.
     * uuid is also the sender stored in the DB.
     */
    if (exp === Action.INSERT_UUID) {
      const uuid = uuidv1();
      setuserDefaults({ sender: uuid, userTheme: userTheme });
      pyShell.send(createDefaultsData(uuid, userTheme, Action.INSERT));
    }
    /**
     * if user Changes his Theme the Theme preference will be refreshed inside the DB.
     */
    if (exp === Action.UPDATE_THEME) {
      pyShell.send(createDefaultsData(sender, userTheme, Action.INSERT));
    }

    pyShell.on("message", message => {
      console.log(message);
      /**
       * case: no data is held in the userDefaults in DB.
       * Recursively calling this Function again when no data provided
       * with exp insertUUID to insert into DB and create a uuid.
       */
      if (message.length === 0) {
        pyConnections.userDefaultsHandler(
          { sender: sender, userTheme: userTheme },
          setuserDefaults,
          Action.INSERT_UUID
        );
      } else if (exp === Action.INITIAL) {
        /**
         * data is already present in the DB.
         * storing response in its attendant state.
         * */
        setuserDefaults({
          sender: message[0].value,
          userTheme: message[1].value === "True"
        });
      }
    });

    //   end the input stream and allow the process to exit
    pyShell.end((err, code, signal) => {
      if (err) throw err;
      console.log(
        `Python File userDefaultsHandler.py ended with code: ${code} and signal: ${signal}`
      );
    });
  }
};

/**
 * @param {String} fileName Python file in ./app/communicate folder!! without .py!!
 * @param {['json', 'text']} mode specifies the mode the data is send to Python
 * @returns {'PythonShell'} pyShell returns a Python Shell instance
 */
const createPythonCon = (fileName, mode) => {
  return new PythonShell(
    join(__dirname, "..", "communicate", `${fileName}.py`),
    {
      mode: mode
    }
  );
};
