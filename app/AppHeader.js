import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { AppBar, Toolbar, Typography, IconButton } from "@material-ui/core";
import Brightness4Icon from "@material-ui/icons/Brightness4";
import Brightness4OutlinedIcon from "@material-ui/icons/Brightness4Outlined";

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
          <IconButton
            size="medium"
            onClick={() => setprefersDarkMode(!prefersDarkMode)}
          >
            {prefersDarkMode ? (
              <Brightness4Icon />
            ) : (
              <Brightness4OutlinedIcon />
            )}
          </IconButton>
        </Toolbar>
      </AppBar>
    </div>
  );
};
