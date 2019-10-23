import React, { useState } from "react";
import { Button, TextField, Grid, Container, Box } from "@material-ui/core";
import SendTwoToneIcon from "@material-ui/icons/SendTwoTone";
import { makeStyles } from "@material-ui/core/styles";
import { PythonShell } from "python-shell";

const useStyles = makeStyles(theme => ({
  container: {
    display: "flex",
    flexWrap: "wrap"
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: "70%"
  },
  dense: {
    marginTop: theme.spacing(2)
  },
  menu: {
    width: 200
  }
}));

export const ChatInput = () => {
  const classes = useStyles();
  const [text, settext] = useState(String);
  // let pyshell = new PythonShell("./worker.py");

  const submitText = event => {
    if (text) {
      // pyshell.send(text);
    }
    event.preventDefault();
  };

  const handleChange = event => {
    settext(event.target.value);
  };

  return (
    <Container direction="column" justify="space-around" alignitems="flex-end">
      <form onSubmit={handleChange}>
        <TextField
          id="outlined-multiline-static"
          label="InfraChat"
          multiline
          rows="2"
          margin="normal"
          variant="outlined"
          className={classes.textField}
          onChange={event => settext(event.target.value)}
        />
        <Button
          size="large"
          variant="contained"
          color="secondary"
          onClick={submitText}
          endIcon={<SendTwoToneIcon />}
        >
          SEND
        </Button>
      </form>
    </Container>
  );
};
