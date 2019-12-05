export const Action = {
  LOAD: 1,
  INITIAL: 2,
  ENTRY: 3,
  LOAD_MORE: 4,
  ID: 5,
  CHECK: 6,
  INSERT_UUID: 7,
  UPDATE_THEME: 8,
  INSERT: 9,
  ERROR: "error",
  INFO: "info",
  LOCAL_ARDUINO_STATE: "localArduinoState",
  EXTERNAL_ARDUINO_STATE: "externalArduinoState",
  SHOULD_UPDATE_MESSAGES: "shouldUpdateMessages",
  NEW_MESSAGES: "newMessages"
};

export const SnackBarStyle = {
  SUCCESS: "success",
  WARNING: "warning",
  INFO: "info",
  ERROR: "error"
};

export const printLoggingOrErrorMessages = res => {
  if (res.hasOwnProperty(Action.ERROR)) {
    console.error(res);
    return;
  }
  if (res.hasOwnProperty(Action.INFO)) {
    console.info(res);
  }
};
