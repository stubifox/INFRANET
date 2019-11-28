/**
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:49:16
 * @modify date 2019-11-28 22:49:16
 * @desc [description]
 */
import React, { useState, useEffect, useRef } from "react";
import { Box, Grid, Fab, Tooltip, IconButton } from "@material-ui/core";
import { pyConnections } from "./utils.js";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import { ChatMessages } from "./ChatMessages";
import AutorenewIcon from "@material-ui/icons/Autorenew";

export const ChatWindow = props => {
  const {
    messages,
    setmessages,
    exp,
    setexp,
    arduinoConnectedToSerial,
    sender
  } = props;
  const bottomRef = useRef();
  const [scrollButton, showscrollButton] = useState(false);

  /**
   * on App load:
   * - calling function for checking if a DB is present.
   * -  getting stored Messages from DB if a Device is connected to the Serial Bus.
   * - scrolling to Button of Messages
   *
   */
  useEffect(() => {
    if (!arduinoConnectedToSerial) {
      pyConnections.insertIntoDb("", "", "initial");
      pyConnections.getFromDb("initial", setmessages, messages);
      setexp("initial");
    }
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
    bottomRef.current.scrollIntoView({ behavior: "smooth" });
  };

  /**
   *
   * @param {'event'} event n MouseWheelScrollUp
   */
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
    <Box style={{ overflow: "hidden" }} onWheel={handleScroll}>
      <Grid container direction="column" alignItems="center" justify="flex-end">
        {!!messages.length && (
          <Tooltip title="Load Older Messages" placement="left">
            <IconButton onClick={loadOlderMessages} color="primary">
              <AutorenewIcon />
            </IconButton>
          </Tooltip>
        )}
        <ChatMessages messages={messages} sender={sender} />
        <Grid
          container
          direction="column"
          justify="flex-end"
          alignItems="center"
          style={{ position: "fixed", bottom: window.innerHeight * 0.2 }}
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
      </Grid>
      <Box ref={bottomRef} />
    </Box>
  );
};
