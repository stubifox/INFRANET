import React from "react";
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
  const { prefersDarkMode, setprefersDarkMode } = props;
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = event => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <Tooltip title="More" placement="left">
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
          <Typography variant="subtitle1">Enable Dark Mode</Typography>
          <Switch
            color="secondary"
            onClick={() => setprefersDarkMode(!prefersDarkMode)}
          />
        </MenuItem>
      </Menu>
    </div>
  );
};
