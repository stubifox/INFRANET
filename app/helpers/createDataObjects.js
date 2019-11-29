/**
 * @param {string} message appending message to an obj
 * @param {string} sender apppending sender to an obj
 * @param {string} exp appending the expression to an obj
 * @returns {'object'}  a object obj for communication with python
 */
const createData = (message, sender, exp) => ({
  message: message,
  sender: sender,
  load: exp
});

/**
 * @exports
 * @param {string} exp the expression, appending to an obj
 * @param {number} id the id, appending to an obj
 * @param {string} receiver the receiver (chatpartner), appending to an obj
 * @returns {'object'}  a object obj for communication with python
 */
const createReceivingData = (exp, id) => ({
  load: exp,
  id: id
});

/**
 * @param {'uuid'} uuid the identifier to append to the obj
 * @param {boolean} userTheme the specified user theme to append to the obj
 * @param {string} exp expression append to obj
 * @returns {'object'}  a object for communication with python.
 */
const createDefaultsData = (uuid, userTheme, exp) => ({
  uuid: uuid,
  theme: userTheme,
  load: exp
});

export { createData, createDefaultsData, createReceivingData };
