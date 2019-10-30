"use babel";

import React, { useState, useEffect } from "react";
import { Box, IconButton } from "@material-ui/core";
import { ThemeProvider } from "@material-ui/styles";
import { ChatInput } from "./ChatInput";
import { ChatWindow } from "./ChatWindow";
import { createMuiTheme } from "@material-ui/core/styles";
import { purple } from "@material-ui/core/colors";

import { AppHeader } from "./AppHeader";

const App = () => {
  const [prefersDarkMode, setprefersDarkMode] = useState(false);
  const [messages, setmessages] = useState([]);
  const [arduinoID, setarduinoID] = useState(String);
  const [aliasName, setaliasName] = useState(String);
  const [exp, setexp] = useState(String);

  const userTheme = createMuiTheme({
    palette: {
      type: prefersDarkMode ? "dark" : "light",
      primary: { main: purple[500] },
      secondary: { main: "#11cb5f" },
      background: {
        default: prefersDarkMode ? "#121212" : "#ffff"
      }
    }
  });

  return (
    <ThemeProvider theme={userTheme}>
      <AppHeader
        prefersDarkMode={prefersDarkMode}
        setprefersDarkMode={setprefersDarkMode}
      />
      <Box
        style={{
          minHeight: window.innerHeight
        }}
        bgcolor={userTheme.palette.background.default}
      >
        <ChatWindow
          theme={userTheme}
          messages={messages}
          setmessages={setmessages}
          exp={exp}
          setexp={setexp}
        />
        <ChatInput
          theme={userTheme}
          messages={messages}
          setmessages={setmessages}
          setexp={setexp}
        />
      </Box>
    </ThemeProvider>
  );
};
export default App;
