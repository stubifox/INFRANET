import React, { useState } from "react";
import { TextField, Container, IconButton, Box } from "@material-ui/core";
import SendIcon from "@material-ui/icons/Send";
import { makeStyles } from "@material-ui/core/styles";
import { sendTextToPython, createData } from "./utils";

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
  const classes = useStyles();
  const [text, settext] = useState(String);
  const [error, seterror] = useState(false);

  const submitText = event => {
    if (text) {
      sendTextToPython(text);
      settext("");
    }
    event.preventDefault();
  };

  const handleChange = event => {
    settext(event.target.value);
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
                <IconButton size="medium" onClick={submitText}>
                  <SendIcon color="primary" />
                </IconButton>
              )
            }}
          />
        </form>
      </Container>
    </Box>
  );
};