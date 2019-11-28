/**
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:49:11
 * @modify date 2019-11-28 22:49:11
 * @desc [description]
 */

import React from "react";
import { Grid, Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => ({
  time: {
    color: theme.palette.text.hint,
    marginBottom: theme.spacing(1),
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(2)
  },
  date: {
    margin: theme.spacing(1),
    padding: theme.spacing(1),
    position: "static"
    // top: "12.5vh"
  },
  typo: {
    wordBreak: "break-word"
  },
  leftMessage: {
    padding: theme.spacing(1),
    marginLeft: theme.spacing(2),
    marginRight: theme.spacing(1),
    marginTop: theme.spacing(1),
    maxWidth: "60%",
    backgroundColor: theme.palette.primary.light
  },
  rightMessage: {
    padding: theme.spacing(1),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(2),
    marginTop: theme.spacing(1),
    maxWidth: "60%",
    backgroundColor: theme.palette.secondary.light
  }
}));

export const ChatMessages = props => {
  const classes = useStyles();
  let renderDate = String;
  const checkRenderDate = date => {
    if (date === renderDate) {
      return false;
    }
    if (date !== renderDate) {
      renderDate = date;
      return true;
    }
  };

  const { messages, sender } = props;

  return (
    <React.Fragment>
      {messages &&
        messages.map(log => (
          <React.Fragment key={log.id}>
            {checkRenderDate(log.date) && (
              <Paper className={classes.date} square={true}>
                <Typography>{log.date}</Typography>
              </Paper>
            )}
            <Grid
              spacing={0}
              container
              direction="column"
              justify="space-evenly"
              alignItems={log.sender === sender ? "flex-end" : "flex-start"}
            >
              <Paper
                className={
                  log.sender === sender
                    ? classes.rightMessage
                    : classes.leftMessage
                }
              >
                <Grid container direction="row" justify="space-between">
                  <Typography className={classes.typo}>
                    {log.message}
                  </Typography>
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
          </React.Fragment>
        ))}
    </React.Fragment>
  );
};
