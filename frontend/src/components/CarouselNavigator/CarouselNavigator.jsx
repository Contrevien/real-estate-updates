import React from 'react';
import './CarouselNavigator.css';

const CarouselNavigator = (props) => {
    
    const clickableCircles = props.cards.map((c, i) => {
        return <div 
            onClick={() => props.changeCard(i)}
            className={props.current === i ? 
                "CarouselNavigator-clickable-circle clickable-circle-selected" :  "CarouselNavigator-clickable-circle"}
            key={i} 
            pos={i}></div>
    })
    
    return (
        <div className="CarouselNavigator">
            {clickableCircles}
        </div>
    );
};

export default CarouselNavigator;