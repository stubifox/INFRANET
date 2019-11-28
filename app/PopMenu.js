/**
 * @author Max Stubenbord
 * @email max.stubi@googlemail.com
 * @create date 2019-11-28 22:49:29
 * @modify date 2019-11-28 22:49:29
 * @desc [description]
 */

import React, { useState, useEffect } from "react";
import {
  Menu,
  MenuItem,
  Switch,
  IconButton,
  Typography,
  Tooltip
} from "@material-ui/core";
import MoreVertIcon from "@material-ui/icons/MoreVert";

export const PopMenu = props => {
  const { userDefaults, setuserDefaults } = props;
  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = event => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleThemeSwitch = () => {
    setuserDefaults({
      sender: userDefaults.sender,
      userTheme: !userDefaults.userTheme
    });
  };

  return (
    <React.Fragment>
      <Tooltip title="More" placement="bottom">
        <IconButton
          aria-controls="simple-menu"
          aria-haspopup="true"
          onClick={handleClick}
        >
          <MoreVertIcon />
        </IconButton>
      </Tooltip>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem>
          <Typography variant="subtitle1">Switch Theme</Typography>
          <Switch color="secondary" onClick={handleThemeSwitch} />
        </MenuItem>
      </Menu>
    </React.Fragment>
  );
};
