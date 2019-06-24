import React from 'react';
import './Email.css';

const Email = (props) => {
    return (
        <div className="Location">
            <h4>Please enter your Email ID</h4>
            <input type="text" className="Location-search" placeholder="Email.."
                value={props.value} onChange={props.changed} />
            {props.message ? <p className="spl-msg">{props.message}</p> : <p className="spl-msg">&nbsp;</p>}
            <button className="Email-submit" onClick={props.submit}>&#10004;</button>
        </div>
    );
};

export default Email;