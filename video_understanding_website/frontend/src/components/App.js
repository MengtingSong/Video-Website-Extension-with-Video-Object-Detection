import React, { Component } from "react";
import TopLevelClass from "./TopLevelClass"


export default class App extends Component {
  constructor() {
    super();
    this.state = {isAuthenticated : false};
  }

  render() {
    return (
      <React.Fragment>
        <TopLevelClass ></TopLevelClass>
      </React.Fragment>
    )
  }
}
