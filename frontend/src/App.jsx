import React from 'react';
import './App.css';
import Loader from './components/Loader/Loader';
import Carousel from './components/Carousel/Carousel';
import Instructions from './components/Instructions/Instructions';
import Showcase from './components/Showcase/Showcase';

class App extends React.Component {
  
  state = {
    loading: true,
    showCase: false
  }

  toggleShowcase = () => {
    let showCase = this.state.showCase;
    this.setState({
      showCase: !showCase
    })
  }

  componentDidMount() {
    setTimeout(() => this.setState({ loading: false }), 1000);
    window.onkeydown = (e) => {
      if(e.key === "Escape") {
        this.setState({
          showCase: false
        })
      }
    }
  }
  
  render() {
    return (
      <div className="App">
        <header>
          <h1 className="App-h1">finden</h1>
          <nav>
              <ul>
                  <li className="App-li" onClick={this.toggleShowcase}>Preview Email</li>
              </ul>
          </nav>
        </header>
        <Carousel />
        <Instructions />
        {this.state.loading && <Loader />}
        {this.state.showCase && 
          <>
            <div className="Backdrop" onClick={this.toggleShowcase}></div>
            <Showcase close={this.toggleShowcase} />
          </>
        }
      </div>
    );
  }
}

export default App;
