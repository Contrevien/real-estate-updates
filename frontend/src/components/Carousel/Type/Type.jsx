import React from 'react';
import './Type.css';

const Type = (props) => {
    return (
        <div className="Type">
            <h4>Tell us what you are looking for?</h4>
            <div className="Type-row" onClick={() => props.select("apartment_rent")}>
                <div className="Type-radio">
                    <div className={props.selected === "apartment_rent" ? "Type-fill Type-filled" : "Type-fill"}></div>    
                </div>
                <div className="Type-category">Apartments for rent</div>
            </div>
            <div className="Type-row" onClick={() => props.select("room_rent")}>
                <div className="Type-radio">
                    <div className={props.selected === "room_rent" ? "Type-fill Type-filled" : "Type-fill"}></div>    
                </div>
                <div className="Type-category">Rooms for rent</div>
            </div>
            <div className="Type-row" onClick={() => props.select("apartment_buy")}>
                <div className="Type-radio">
                    <div className={props.selected === "apartment_buy" ? "Type-fill Type-filled" : "Type-fill"}></div>    
                </div>
                <div className="Type-category">Apartments for buying</div>
            </div>
        </div>
    );
};

export default Type;