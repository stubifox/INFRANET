/**
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:48:56
 * @modify date 2019-11-28 22:48:56
 * @desc [description]
 */

import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { AppBar, Toolbar, Typography, Tooltip } from "@material-ui/core";
import PhonelinkEraseIcon from "@material-ui/icons/PhonelinkErase";
import PhonelinkLockIcon from "@material-ui/icons/PhonelinkLock";
import SettingsInputAntennaIcon from "@material-ui/icons/SettingsInputAntenna";
import PortableWifiOffIcon from "@material-ui/icons/PortableWifiOff";

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
  },
  icons: {
    margin: theme.spacing(4)
  }
}));

export const AppHeader = props => {
  const {
    arduinoConnectedToSerial,
    connectionEstablished,
    userDefaults,
    setuserDefaults
  } = props;
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            INFRACHAT
          </Typography>
          {arduinoConnectedToSerial &&
            (connectionEstablished ? (
              <Tooltip title="Connected to Chatpartner!" placement="bottom">
                <SettingsInputAntennaIcon className={classes.icon} />
              </Tooltip>
            ) : (
              <Tooltip title="Not connecetd to Chatpartner!" placement="bottom">
                <PortableWifiOffIcon className={classes.icon} />
              </Tooltip>
            ))}
          {arduinoConnectedToSerial ? (
            <Tooltip title="Secure Connection to Device!" placement="bottom">
              <PhonelinkLockIcon className={classes.icon} />
            </Tooltip>
          ) : (
            <Tooltip title="No Device Connected" placement="bottom">
              <PhonelinkEraseIcon className={classes.icons} />
            </Tooltip>
          )}
          <PopMenu
            userDefaults={userDefaults}
            setuserDefaults={setuserDefaults}
          />
        </Toolbar>
      </AppBar>
    </div>
  );
};
