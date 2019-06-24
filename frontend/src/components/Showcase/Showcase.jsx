import React from 'react';
import './Showcase.css';
import showcase from '../../assets/images/showcase.png';

const Showcase = (props) => {
    return (
        <div className="Showcase">
            <span className="Showcase-close" onClick={props.close}>&times;</span>
            <h2>This is what the EMAIL will look like...</h2>
            <img src={showcase} alt="" />
        </div>
    );
};

export default Showcase;