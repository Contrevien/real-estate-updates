import React, { Component } from 'react';
import './Unsubscribed.css'

class Unsubscribed extends Component {
    state = {
        email: this.props.match.params.email,
        message: 0
    }

    componentDidMount() {
        fetch('/unsubscribe', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: this.state.email
            })
        })
            .then(res => res.json())
            .then(res => {
                if(res === "777") {
                    this.setState({
                        message: 2
                    })
                } else if(res === "666") {
                    this.setState({
                        message: 1
                    })
                }
            })
            .catch(err => {
                this.setState({
                    message: 2
                })
            })
    }
    
    render() {

        let message = this.state.message;
        let toShow = null;

        if(message === 0) {
            toShow = <><h1>You have successfully Unsubscribed from the service.</h1>
            <p>We hope to have helped you!</p></>
        } else if(message === 1) {
            toShow = <><h1>Hmm, Something is fishy</h1>
            <p>Perhaps you visited the wrong link?</p></>
        } else {
            toShow = <h1>Some fault occured, please try again!</h1>
        }

        return (
            <div className="Unsubscribed">
                {toShow}
            </div>
        );
    }
}

export default Unsubscribed;