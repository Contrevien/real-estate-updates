import React, { Component } from 'react';
import './Carousel.css';
import CarouselNavigator from '../CarouselNavigator/CarouselNavigator';
import Type from './Type/Type';
import Location from './Location/Location';
import bg from '../../assets/images/bg.png';
import Extra from './Extra/Extra';
import Email from '../Email/Email';
import right from '../../assets/images/right.png';

class Carousel extends Component {
    
    state = {
        cards: ["", "", ["", ""], ""],
        current: 0,
        locations: [],
        showLocations: [],
        locationSelected: false,
        roomsSelected: false,
        message: "",
        emailError: 0
    }

    changeCard = (n) => {
        this.setState({
            current: n
        })
    }

    handleCategory = (value) => {
        let cards = [...this.state.cards];
        let current = this.state.current;
        cards[0] = value;
        cards[1] = "";
        let roomsSelected = value === "room_rent";
        fetch('/location/' + value)
            .then(res => res.json())
            .then(res => {
                this.setState({
                    locations: res,
                    current: current + 1
                })
            });
        this.setState({
            cards: cards,
            roomsSelected: roomsSelected,
            locationSelected: false
        })
        }

    handleLocation = (e) => {
        let value = e.target.value;
        let cards = [...this.state.cards];
        let locations = [...this.state.locations];
        let showLocations = [];
        cards[1] = value;
        for(let loc of locations) {
            if(loc.toLowerCase().includes(value.toLowerCase())) {
                showLocations.push(loc)
            }
        }
        this.setState({
            cards: cards,
            showLocations: showLocations,
            locationSelected: false
        })
    }

    selectLocation = (value) => {
        let cards = [...this.state.cards];
        let current = this.state.current;
        cards[1] = value;
        this.setState({
            cards: cards,
            locationSelected: true,
            current: current + 1
        })
    }

    handleExtra = (t, e) => {
        let cards = [...this.state.cards]
        let value = e.target.value;
        if(isNaN(value)) return;
        if(t === "price") {
            cards[2][0] = value;
        } else {
            if(value.length > 1) return;
            cards[2][1] = value;
        }
        this.setState({
            cards: cards
        })
    }

    moveExtra = () => {
        let current = this.state.current;
        this.setState({
            current: current + 1
        })
    }

    handleEmail = (e) => {
        let cards = [...this.state.cards];
        cards[3] = e.target.value;
        let value = e.target.value;
        let emailError = 0;
        let emailPat = /[a-zA-Z]+([-\.]?[a-zA-Z0-9]+)?@([a-zA-Z0-9-]+\.)+[a-zA-Z-]{2,3}/;
        if (!emailPat.test(value) || value.split('@')[1].split('.')[1].length > 3) {
            emailError = 1;
        }
        this.setState({
            cards: cards,
            emailError: emailError
        })
    }

    submitEverything = (e) => {
        let cards = [...this.state.cards];
        if(cards[0] === "") {
            this.setState({message: "Please select a category"});
        }
        else if(cards[1] === "") {
            this.setState({message: "Please select a location"});
        }
        else if(cards[3] === "" || this.state.emailError === 1) {
            this.setState({message: "Please check the email"});
        }
        else {
            this.setState({message: ""});
        }
    }

    handleSlide = (type) => {
        let current = this.state.current;
        if(type === "L" && current > 0) {
            this.setState({
                current: current - 1
            })
        }
        if(type === "R" && current < 3) {
            this.setState({
                current: current + 1
            })
        }
    }

    
    render() {

        let elements = [
            <Type selected={this.state ? this.state.cards[0] : ""} select={this.handleCategory} />,
            <Location value={this.state ? this.state.cards[1] : ""} changed={this.handleLocation} locations={this.state.showLocations} selected={this.state.locationSelected} select={this.selectLocation} />,
            <Extra value={this.state ? this.state.cards[2] : ""} changed={this.handleExtra} roomsSelected={this.state.roomsSelected} next={this.moveExtra}/>,
            <Email value={this.state ? this.state.cards[3] : ""} changed={this.handleEmail} submit={this.submitEverything} message={this.state.message}/>
        ]

        let { cards, current } = this.state;
        let toDisplay = elements[current];

        return (
            <div className="Carousel-cover">
                <div className="Carousel">
                    {toDisplay}
                    <div className="CarouselNavigator-container">
                        <CarouselNavigator cards={cards} current={current} changeCard={this.changeCard} />
                    </div>
                    <div className="Carousel-controls-left">
                        <img className="Carousel-controls-arrow-left" onClick={() => this.handleSlide("L")} src={right} alt="<" />
                    </div>
                    <div className="Carousel-controls-right">
                        <img className="Carousel-controls-arrow-right" onClick={() => this.handleSlide("R")} src={right} alt=">" />
                    </div>
                </div>
                <h1 className="Carousel-h1">Immobilien finden</h1>
                <img src={bg} className="Carousel-bg" />
            </div>
        );
    }
}

export default Carousel;