import React from 'react';
import './Location.css';

const Location = (props) => {

    const lis = props.locations.map((loc, i) => {
        return <li key={i} onClick={() => props.select(loc)} className="Location-suggestion-li">{loc}</li>
    })

    return (
        <div className="Location">
            <h4>Search the location you want</h4>
            <div className="Location-main-container">
                <input type="text" className="Location-search" placeholder="Search Location" spellCheck={false}
                    value={props.value} onChange={props.changed} />
                {!props.selected && props.value && <ul className="Location-suggestion-ul">
                    {lis}
                </ul>}
            </div>

        </div>
    );
};

export default Location;