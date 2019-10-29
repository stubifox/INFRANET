import React, { useState, useEffect } from "react";
import { Box, Grid, Fab } from "@material-ui/core";
import { pyConnections } from "./utils.js";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import { ChatMessages } from "./ChatMessages";

export const ChatWindow = props => {
  const { messages, setmessages } = props;

  const bottomRef = React.createRef();
  const [scrollButton, showscrollButton] = useState(false);

  useEffect(() => {
    pyConnections.getFromDb("", setmessages);
    scrollToBottom();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = (behaviour = "auto") => {
    bottomRef.current.scrollIntoView({ behaviour: behaviour });
  };

  const handleScroll = event => {
    if (event.nativeEvent.wheelDelta > 0) {
      showscrollButton(true);
    }
  };

  return (
    <Box style={{ overflow: "hidden" }} onWheel={e => handleScroll(e)}>
      <Grid container direction="column" alignItems="center" justify="flex-end">
        <ChatMessages messages={messages} />
        <Grid
          container
          direction="column"
          justify="flex-end"
          alignItems="center"
          style={{ position: "fixed", bottom: "20vh" }}
        >
          {scrollButton && (
            <Fab
              size="medium"
              aria-label="down"
              onClick={() => {
                scrollToBottom("smooth");
                showscrollButton(false);
              }}
            >
              <ExpandMoreIcon />
            </Fab>
          )}
        </Grid>
        <Box ref={bottomRef}></Box>
      </Grid>
    </Box>
  );
};
