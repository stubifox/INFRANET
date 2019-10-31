import React, { useState, useEffect } from "react";
import { Box, Grid, Fab, Tooltip, IconButton } from "@material-ui/core";
import { pyConnections } from "./utils.js";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import { ChatMessages } from "./ChatMessages";
import AutorenewIcon from "@material-ui/icons/Autorenew";

export const ChatWindow = props => {
  const { messages, setmessages, exp, setexp } = props;
  const bottomRef = React.createRef();
  const [scrollButton, showscrollButton] = useState(false);

  useEffect(() => {
    pyConnections.insertIntoDb("", "", "initial");
    pyConnections.getFromDb("initial", setmessages, messages);
    setexp("initial");
    if (exp !== "loadMore") {
      scrollToBottom();
    }
  }, []);

  useEffect(() => {
    if (exp !== "loadMore") {
      scrollToBottom();
    }
  }, [messages]);

  const scrollToBottom = () => {
    bottomRef.current.scrollIntoView({ behaviour: "smooth" });
  };

  const handleScroll = event => {
    if (event.nativeEvent.wheelDelta > 0) {
      showscrollButton(true);
    }
  };
  const loadOlderMessages = () => {
    pyConnections.getFromDb("loadMore", setmessages, messages);
    setexp("loadMore");
  };

  return (
    <Box style={{ overflow: "hidden" }} onWheel={e => handleScroll(e)}>
      <Grid container direction="column" alignItems="center" justify="flex-end">
        <Tooltip title="Load Older Messages" placement="left">
          <IconButton onClick={loadOlderMessages} color="primary">
            <AutorenewIcon />
          </IconButton>
        </Tooltip>
        <ChatMessages messages={messages} />
        <Grid
          container
          direction="column"
          justify="flex-end"
          alignItems="center"
          style={{ position: "fixed", bottom: "20vh" }}
        >
          {scrollButton && (
            <Tooltip title="Scroll Down" placement="top">
              <Fab
                size="medium"
                aria-label="down"
                onClick={() => {
                  scrollToBottom();
                  showscrollButton(false);
                }}
              >
                <ExpandMoreIcon />
              </Fab>
            </Tooltip>
          )}
        </Grid>
        <Box ref={bottomRef}></Box>
      </Grid>
    </Box>
  );
};
