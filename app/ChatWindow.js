import React, { useState, useEffect } from "react";
import { Box, Grid, Paper, Typography } from "@material-ui/core";
import chatLog from "../Log/chatLog.json";
import { makeStyles } from "@material-ui/core/styles";
import { getFromDb, pyConnections } from "./utils.js";

const useStyles = makeStyles(theme => ({
  typo: {
    wordBreak: "break-word"
  },
  leftMessage: {
    padding: theme.spacing(1),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    marginTop: theme.spacing(2),
    maxWidth: "40%",
    backgroundColor: theme.palette.primary.light
  },
  rightMessage: {
    padding: theme.spacing(1),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    marginTop: theme.spacing(2),
    maxWidth: "40%",
    backgroundColor: theme.palette.secondary.light
  }
}));

export const ChatWindow = props => {
  const { messages, setmessages } = props;

  const classes = useStyles();
  const bottomRef = React.createRef();

  useEffect(() => {
    pyConnections.getFromDb("", setmessages);
    scrollToBottom();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    bottomRef.current.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <Box>
      {messages &&
        messages.map(log => (
          <Grid
            key={log.id}
            spacing={0}
            container
            className={classes.box}
            direction="column"
            justify="space-evenly"
            alignItems={log.sender === "max" ? "flex-end" : "flex-start"}
          >
            <Paper
              className={
                log.sender === "max"
                  ? classes.rightMessage
                  : classes.leftMessage
              }
            >
              <Grid container direction="row" justify="space-between">
                <Typography className={classes.typo}>{log.message}</Typography>
                <Typography align="right">{log.time}</Typography>
              </Grid>
            </Paper>
          </Grid>
        ))}
      <Box ref={bottomRef} />
    </Box>
  );
};
