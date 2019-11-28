/**
 * author: Max Stubenbord
 */

import { PythonShell } from "python-shell";
import { join } from "path";
import uuidv1 from "uuid";

/**
 * different Functions to communicate with Python Scripts
 * states are being updated depending on returning message of the Scripts
 *
 * Communication realized via Stdin and Stdout.
 * protocol for communication is JSON.
 */
export const pyConnections = {
  /**
   * @param {['initial', '']} exp an expression to say the func what to do, NOT REQUIRED!
   * @param {string} message the  message to insert into the db
   * @param {string} sender the sender to insert into the db
   */

  insertIntoDb: (message, sender, exp = "") => {
    const pyShell = createPythonCon("dataBaseConnection", "json");
    /**
     * on initial App load just check if DB is existent.
     */

    if (exp === "initial") {
      pyShell.send(createData("", "", exp));
    } else {
      /**
       * normal message input received. put message and sender into DB.
       */
      pyShell.send(createData(message, sender, exp));
    }

    pyShell.on("message", message => {
      console.log(`insertIntoDB with: ${message}`);
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
   * @param {'function'} setstateFunc a state Function to update the state
   * @param {'React.state'} state the corresponding state to the state Function
   */

  getFromDb: async (exp, setstateFunc, state) => {
    const pyShell = createPythonCon("getFromDb", "json");

    /**
     * load more entries out of DB starting with id at index 0 of current message Array.
     */
    if (exp === "loadMore") {
      pyShell.send({ load: exp, id: state[0].id });
    } else {
      /**
       * load last 20 messages out of DB.
       */
      pyShell.send({ load: exp });
    }

    await pyShell.on("message", response => {
      /**
       * initial load message Array is just filled with whole response (20 messages)
       */
      if (exp === "initial") {
        setstateFunc(response);

        /**
         * getting the last inserted Message out of DB.
         * happens when user inputs a message.
         */
      } else if (exp === "entry") {
        setstateFunc([...state, response[0]]);
        /**
         * user wants to load more messages starting from top.
         * will be appended in front of current state.
         */
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
    if (exp === "initial") {
      pyShell.send(createDefaultsData("", "", "check"));
    }

    /**
     * if no data is deposited, insert Data into DB
     * also create a UUID for identification purposes.
     * uuid is also the sender stored in the DB.
     */
    if (exp === "insertUUID") {
      const uuid = uuidv1();
      pyShell.send(createDefaultsData(uuid, userTheme, "insert"));
    }
    /**
     * if user Changes his Theme the Theme preference is also stored in the DB.
     */
    if (exp === "updateTheme") {
      pyShell.send(createDefaultsData(sender, userTheme, "insert"));
    }

    pyShell.on("message", message => {
      /**
       * case: no data is held in the userDefaults in DB.
       * Calling this Function again with exp insertUUID to insert into DB and create a uuid.
       */
      if (message.length === 0) {
        console.log("message is indeed empty");
        pyConnections.userDefaultsHandler(
          { sender: sender, userTheme: userTheme },
          setuserTheme,
          "insertUUID"
        );
      } else if (exp === "initial") {
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
 *
 * @param {String} fileName Python file in ./app/communicate folder!! without .py!!
 * @param {['json', 'text']} mode specifies the mode the data is send to Python
 * @returns {'PythonShell'} pyShell returns a Python Shell instance
 */
const createPythonCon = (fileName, mode) => {
  return new PythonShell(join(__dirname, "communicate", `${fileName}.py`), {
    mode: mode
  });
};

/**
 *
 * @param {string} message appending message to an obj
 * @param {string} sender apppending sender to an obj
 * @param {string} exp appending the expression to an obj
 * @returns {'object'} {} a object obj for communication with python
 */
const createData = (message, sender, exp) => ({
  message: message,
  sender: sender,
  load: exp
});

/**
 *
 * @param {'uuid'} uuid the identifier to append to the obj
 * @param {boolean} userTheme the specified user theme to append to the obj
 * @param {string} exp expression append to obj
 * @returns {'object'} {} a object for communication with python.
 */
const createDefaultsData = (uuid, userTheme, exp) => ({
  uuid: uuid,
  theme: userTheme,
  load: exp
});
