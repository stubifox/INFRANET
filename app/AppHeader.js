import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { AppBar, Toolbar, Typography } from "@material-ui/core";

import { PopMenu } from "./PopMenu";

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
    position: "sticky",
    top: 0
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1
  }
}));

export const AppHeader = props => {
  const { prefersDarkMode, setprefersDarkMode } = props;
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            INFRACHAT
          </Typography>
          <PopMenu
            prefersDarkMode={prefersDarkMode}
            setprefersDarkMode={setprefersDarkMode}
          />
        </Toolbar>
      </AppBar>
    </div>
  );
};
