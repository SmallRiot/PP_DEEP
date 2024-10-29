import { Outlet } from "react-router-dom";
// import Card from "../Card/Card";
import Subsequence from "../Subsequence/Subsequence";
import classes from "./BankPage.module.css";

const BankPage = () => {
  return (
    <div>
      <div className={classes.wrapper}>
        <div className={classes.title}>
          <p>Компенсация при оплате работником Банка франшизы</p>
        </div>
        <Subsequence count={8} />
      </div>
      <Outlet />
      {/* <Card /> */}
    </div>
  );
};

export default BankPage;
