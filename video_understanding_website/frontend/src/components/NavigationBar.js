import React, { Component } from "react";
import { Link } from "react-router-dom";
import { UserContext } from "./UserProvider";

import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import AccountCircle from '@material-ui/icons/AccountCircle';
import Button from '@material-ui/core/Button';
import HomeIcon from '@material-ui/icons/Home';

const useStyles = theme => ({
    root: {
      flexGrow: 1,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
});

class NavigationBar extends Component {
    constructor(props) {
        super(props);
    }

    handleLogout = () => {
        let user = this.context;
        delete localStorage.accessToken;
        user.setAuth(false);
    }

    render() {
        let user = this.context;
        const { classes } = this.props;

        return (
        <div>
        <AppBar>
            <Toolbar>
            <IconButton edge="start" className={classes.menuButton} color="inherit" component={Link} to="/">
                <HomeIcon />
            </IconButton>
            <Typography variant="h6" className={classes.title}>
                Video Object Detection
            </Typography>
            {user.state.isAuthenticated? (
                <div>
                <IconButton
                    aria-label="account of current user"
                    aria-controls="menu-appbar"
                    aria-haspopup="true"
                    component={Link}
                    to="/profile"
                    color="inherit"
                >
                    <AccountCircle />
                </IconButton>
                <Button component={Link} to="/" onClick={this.handleLogout} color="inherit">Logout</Button>
                </div>
            ):
            <Button component={Link} to="/signIn" color="inherit">Login</Button>}
            </Toolbar>
        </AppBar>
        </div>
        )
    }
}

NavigationBar.contextType = UserContext;
export default withStyles(useStyles)(NavigationBar);
