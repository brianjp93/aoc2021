import "./App.css";
import { Routes, Route, Link } from "react-router-dom";
import { Day1 } from "./components/days/day1";
import { Day2 } from "./components/days/day2";
import "bootstrap/dist/css/bootstrap.css";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/day/1/" element={<Day1/>} />
        <Route path="/day/2/" element={<Day2/>} />
      </Routes>
    </div>
  );
}

function Home() {
  return (
    <>
      <div className="container">
        <h1>Welcome home.</h1>
        <div className="row col">
          <Link to='/day/1/' >Day 1</Link>
        </div>
        <div className="row col">
          <Link to='/day/2/' >Day 2</Link>
        </div>
      </div>
    </>
  );
}

export default App;
