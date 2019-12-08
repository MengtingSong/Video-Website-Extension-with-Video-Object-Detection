import React, { Component } from "react";
import {AWS_credentials} from "../../AWS_keys";

const config = {
        bucketName : 'miniproj3videos',
        dirName: 'test@gmail.com',
        region: 'us-east-2',
        accessKeyId: AWS_credentials.accessKeyId,
        secretAccessKey: AWS_credentials.secretAccessKey
        };

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render(){
        return (
            <div>
                <h3>
                    Upload an video file
                </h3>
                <input
                type = "file"
                onChange = {this.upload}
                />
            </div>
                );
        }
}

