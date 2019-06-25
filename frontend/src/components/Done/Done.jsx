import React from 'react';
import './Done.css';
import bg from '../../assets/images/bg.png';

const Done = (props) => {
    return (
        <div className="Done">
            <div><span>&#10004;</span></div>
            <img src={bg} alt="" className="Done-show" onLoad={props.loaded} />
            <h1>You have successfully subscribed to our service!</h1>
            <p>Check your mailbox for details and confirmation</p>
        </div>
    );
};

export default Done;