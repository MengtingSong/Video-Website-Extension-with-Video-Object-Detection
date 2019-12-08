import React, { Component } from "react";

const config = {
        bucketName : 'googleaudio',
        dirName: 'user2gmail.com',
        region: 'us-east-2',
        accessKeyId: 'AKIAVJ45X5OX3IQLFQ6D',
        secretAccessKey: '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'
        };

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render(){
        return (
            <div>
                <h3>
                    Upload an audio file
                </h3>
                <input
                type = "file"
                onChange = {this.upload}
                />
            </div>
                );
        }
}

