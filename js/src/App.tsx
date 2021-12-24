import "./App.css";
import { Routes, Route } from "react-router-dom";
import { Day1 } from "./components/days/day1";
import "bootstrap/dist/css/bootstrap.css";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/day/1/" element={<Day1/>} />
      </Routes>
    </div>
  );
}

function Home() {
  return (
    <>
      <div className="container">
        <h1>Welcome home.</h1>
      </div>
    </>
  );
}

export default App;
