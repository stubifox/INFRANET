/**
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:49:02
 * @modify date 2019-11-28 22:49:02
 * @desc [description]
 */

import React, { useState } from "react";
import {
  TextField,
  Container,
  IconButton,
  Box,
  InputAdornment,
  Typography
} from "@material-ui/core";
import SendIcon from "@material-ui/icons/Send";
import { makeStyles } from "@material-ui/core/styles";
import { pyConnections } from "./helpers/pyConnections";
import { Action } from "./helpers/shared";

const useStyles = makeStyles(theme => ({
  box: {
    position: "sticky",
    bottom: 0
  },
  container: {
    bottom: 0,
    backgroundColor: theme.palette.background.default,
    maxWidth: "none"
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1)
  }
}));

export const ChatInput = props => {
  const {
    messages,
    setmessages,
    setexp,
    arduinoConnectedToSerial,
    handleShowSnackBar,
    connectionEstablished,
    sender
  } = props;
  const classes = useStyles();

  const [text, settext] = useState(String);
  const [error, seterror] = useState(false);
  const MAX_MESSAGE_LENGTH = 280;

  const submitText = event => {
    if (arduinoConnectedToSerial && connectionEstablished && text) {
      seterror(false);
      pyConnections.insertIntoDb(text, sender, Action.INSERT);
      pyConnections.getFromDb(Action.ENTRY, setmessages, messages);
      setexp(Action.ENTRY);
      settext("");
    } else if (text) {
      handleErrors();
    }
    event.preventDefault();
  };

  const handleChange = event => {
    if (event.target.value.length <= MAX_MESSAGE_LENGTH) {
      settext(event.target.value);
    }
  };
  const handleErrors = () => {
    seterror(true);
    if (!arduinoConnectedToSerial) {
      handleShowSnackBar("No Device connected to USB!", "error");
    }
    if (arduinoConnectedToSerial && !connectionEstablished) {
      handleShowSnackBar("Not connected to Chatpartner!", "error");
    }
    setTimeout(() => seterror(false), 4000);
  };

  return (
    <Box className={classes.box}>
      <Container
        direction="column"
        justify="space-around"
        alignitems="flex-end"
        className={classes.container}
      >
        <form onSubmit={submitText}>
          <TextField
            error={error}
            color="secondary"
            fullWidth
            id="outlined-multiline-static"
            label="Send Text"
            multiline
            rows="2"
            margin="normal"
            variant="outlined"
            className={classes.textField}
            onChange={handleChange}
            value={text}
            onKeyDown={event => {
              if (event.key === "Enter" && !event.shiftKey) submitText(event);
            }}
            InputProps={{
              endAdornment: (
                <InputAdornment>
                  <Typography>
                    {text.length}/{MAX_MESSAGE_LENGTH}
                  </Typography>
                  <IconButton size="medium" onClick={submitText}>
                    <SendIcon color="primary" />
                  </IconButton>
                </InputAdornment>
              )
            }}
          />
        </form>
      </Container>
    </Box>
  );
};
