/**
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:48:38
 * @modify date 2019-11-28 22:48:38
 * @desc [description]
 */

"use babel";

import React, { useState, useEffect } from "react";
import { Box, Grid } from "@material-ui/core";
import { ThemeProvider } from "@material-ui/styles";
import { ChatInput } from "./ChatInput";
import { ChatWindow } from "./ChatWindow";
import { createMuiTheme } from "@material-ui/core/styles";
import { purple } from "@material-ui/core/colors";
import { AppHeader } from "./AppHeader";
import { CustomizedSnackbar } from "./CustomSnackBar";
import { pyConnections } from "./helpers/pyConnections";
import { Action, SnackBarStyle } from "./helpers/shared";

const App = () => {
  /**
   * STATE DECLARATIONS
   */
  const [messages, setmessages] = useState([]);
  const [externalStates, setexternalStates] = useState({
    internalArduinoConnected: true,
    externalArduinoConnected: true,
    newMessagesArrived: false,
    chatPartnerUUID: String
  });
  //set initial states to false when implemented
  const [exp, setexp] = useState(String);
  const defaultStateSnackBar = {
    display: false,
    message: String,
    variant: String
  };
  const [userDefaults, setuserDefaults] = useState({
    sender: String,
    userTheme: true
  });
  const [displaySnackBar, setdisplaySnackBar] = useState(defaultStateSnackBar);
  /**
   * END OF STATE DECLARATIONS
   */
  /**
   *
   * @param {string} message message to display in the Snackbar
   * @param {SnackBarStyle} variant styling of SnackBar
   * @param {number} timeout optional timeout
   */
  const handleShowSnackBar = (message, variant, timeout = 4000) => {
    setdisplaySnackBar({ display: true, message: message, variant: variant });
    setTimeout(() => setdisplaySnackBar(defaultStateSnackBar), timeout);
  };

  const userTheme = createMuiTheme({
    palette: {
      type: userDefaults.userTheme ? "dark" : "light",
      primary: { main: purple[500] },
      secondary: { main: "#11cb5f" },
      background: {
        default: userDefaults.userTheme ? "#121212" : "#fff"
      }
    }
  });

  const askForStates_600 = () => {
    setInterval(
      () =>
        pyConnections.getExternalStateChanges(
          externalStates,
          setexternalStates,
          messages,
          Action.INITIAL
        ),
      600
    );
  };

  useEffect(() => {
    pyConnections.insertIntoDb("", "", Action.INITIAL);
    pyConnections.userDefaultsHandler(
      userDefaults,
      setuserDefaults,
      Action.INITIAL
    );
    //remove when states are there!!
    pyConnections.getFromDb(Action.INITIAL, setmessages, messages);
    setexp(Action.INITIAL);
  }, []);

  //calling every 600ms
  useEffect(() => {
    askForStates_600();
    return () => {
      clearInterval(askForStates_600);
    };
  }, []);

  const askForStatesWithID = () => {
    setInterval(
      () =>
        pyConnections.getExternalStateChanges(
          externalStates,
          setexternalStates,
          messages,
          Action.ID
        ),
      600
    );
  };

  useEffect(() => {
    if (messages.length > 0) {
      clearInterval(askForStates_600);
      askForStatesWithID();
    }
    return () => clearInterval(askForStatesWithID)
  }, [])

  // useEffect(() => {
  //   if (
  //     externalStates.internalArduinoConnected &&
  //     externalStates.internalArduinoConnected
  //   ) {
  //     pyConnections.getFromDb(Action.INITIAL, setmessages, messages);
  //     setexp(Action.INITIAL);
  //   }
  // }, [userDefaults.sender]);

  /**
   * display SnackBars when connection to either Device on USB is established
   * or connection to Chat Partner is established
   */
  useEffect(() => {
    externalStates.internalArduinoConnected
      ? handleShowSnackBar("Device connected to USB!", SnackBarStyle.SUCCESS)
      : handleShowSnackBar("No device connected to USB!", SnackBarStyle.ERROR);

    externalStates.internalArduinoConnected &&
      (externalStates.externalArduinoConnected
        ? handleShowSnackBar("Connected to Chatpartner", SnackBarStyle.SUCCESS)
        : handleShowSnackBar(
          "Not connected to Chatpartner!",
          SnackBarStyle.WARNING
        ));
  }, [
    externalStates.internalArduinoConnected,
    externalStates.externalArduinoConnected
  ]);

  useEffect(() => {
    pyConnections.userDefaultsHandler(
      userDefaults,
      setuserDefaults,
      Action.UPDATE_THEME
    );
  }, [userDefaults.userTheme]);

  return (
    <ThemeProvider theme={userTheme}>
      {displaySnackBar.display && (
        <CustomizedSnackbar
          message={displaySnackBar.message}
          variant={displaySnackBar.variant}
        />
      )}

      <Grid
        container
        direction="column"
        justify="flex-start"
        alignItems="stretch"
        style={{
          minHeight: window.innerHeight,
          background: userTheme.palette.background.default
        }}
      >
        <AppHeader
          externalStates={externalStates}
          userDefaults={userDefaults}
          setuserDefaults={setuserDefaults}
        />
        <ChatWindow
          externalStates={externalStates}
          messages={messages}
          setmessages={setmessages}
          exp={exp}
          setexp={setexp}
          sender={userDefaults.sender}
        />
        <ChatInput
          sender={userDefaults.sender}
          externalStates={externalStates}
          messages={messages}
          setmessages={setmessages}
          setexp={setexp}
          handleShowSnackBar={handleShowSnackBar}
        />
      </Grid>
    </ThemeProvider>
  );
};
export default App;
