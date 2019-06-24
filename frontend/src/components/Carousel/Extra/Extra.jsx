import React from 'react';
import './Extra.css';
import right from '../../../assets/images/right.png';

const Extra = (props) => {

    let price = props.value[0]
    let rooms = props.value[1]

    return (
        <div className="Extra">
            <h4>Max Price and Number of Room(s)</h4>
            <div className="Extra-row">
                <input type="text" className="Extra-input" placeholder="Max Price"
                    value={price} onChange={(e) => props.changed("price", e)} />
                <span>&euro;</span>
            </div>
            <div className="Extra-row">
                <input type="text" disabled={props.roomsSelected} className="Extra-input" placeholder="Number of rooms" 
                    value={props.roomsSelected ? "1" : rooms} onChange={(e) => props.changed("rooms", e)} />
                <span>Zi.</span>
            </div>
            <div className="Extra-row">
                <button className="Extra-next" onClick={props.next}>
                    <img src={right} alt=">" />
                </button>
            </div>
        </div>
    );
};


export default Extra;