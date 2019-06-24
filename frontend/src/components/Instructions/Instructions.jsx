import React from 'react';
import './Instructions.css';
import checklist from '../../assets/images/checklist.png';
import email from '../../assets/images/email.png';
import enter from '../../assets/images/enter.png';
import right from '../../assets/images/right.png';

const Instructions = () => {
    return (
        <div className="Instructions">
            <div className="Instructions-col Instructions-first">
                <img src={checklist} alt="" className="Instructions-img"/>
                <p>Select your preferences</p>
            </div>
            <img src={right} alt="" className="Instructions-right" />
            <div className="Instructions-col Instructions-center">
                <img src={enter} alt="" className="Instructions-spl" />
                <p>Enter your email ID</p>
            </div>
            <img src={right} alt="" className="Instructions-right"/>
            <div className="Instructions-col Instructions-last">
                <img src={email} alt="" className="Instructions-img"/>
                <p>Check your mail for updates</p>
            </div>
        </div>
    );
};

export default Instructions;