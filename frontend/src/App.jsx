import React from 'react';
import './App.css';
import Loader from './components/Loader/Loader';
import Carousel from './components/Carousel/Carousel';
import Instructions from './components/Instructions/Instructions';
import Showcase from './components/Showcase/Showcase';
import Done from './components/Done/Done';

class App extends React.Component {
  
  state = {
    loading: true,
    showCase: false,
    done: false
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

  getDone = () => {
    this.setState({
      loading: true,
      done: true
    })
  }

  toggleLoader = () => {
    let curr = this.state.loading;
    
    this.setState({
      loading: !curr
    })
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
        <Carousel done={this.getDone} loader={this.toggleLoader} />
        <Instructions />
        {this.state.loading && <Loader />}
        {this.state.showCase && 
          <>
            <div className="Backdrop" onClick={this.toggleShowcase}></div>
            <Showcase close={this.toggleShowcase} />
          </>
        }
        {this.state.done && <Done loaded={this.toggleLoader} />}
      </div>
    );
  }
}

export default App;
