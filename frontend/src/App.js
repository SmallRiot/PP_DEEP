import "./App.css";
import Header from "./components/Header/Header";
import Start from "./components/Start/Start";
import BankPage from "./components/BankPage/BankPage";
import { Route, Routes } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="" element={<Start />}></Route>
        <Route path="bank" element={<BankPage />} />
        {/* <Start /> */}
      </Routes>
    </div>
  );
}

export default App;
