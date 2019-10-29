import React from "react";
import { Grid, Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  time: {
    color: theme.palette.text.hint,
    marginBottom: theme.spacing(1),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1)
  },
  typo: {
    wordBreak: "break-word"
  },
  leftMessage: {
    padding: theme.spacing(1),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    marginTop: theme.spacing(1),
    maxWidth: "60%",
    backgroundColor: theme.palette.primary.light
  },
  rightMessage: {
    padding: theme.spacing(1),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    marginTop: theme.spacing(1),
    maxWidth: "60%",
    backgroundColor: theme.palette.secondary.light
  }
}));

export const ChatMessages = props => {
  const classes = useStyles();

  const { messages } = props;

  return (
    <div>
      {messages &&
        messages.map(log => (
          <Grid
            key={log.id}
            spacing={0}
            container
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
              </Grid>
            </Paper>
            <Typography
              variant="button"
              className={classes.time}
              align={log.sender === "max" ? "right" : "left"}
            >
              {log.time}
            </Typography>
          </Grid>
        ))}
    </div>
  );
};
