import { Link } from "react-router-dom";
import SubmitButton from "../SubmitButton/SubmitButton";
import classes from "./SelectBlock.module.css";

const SelectBlock = () => {
  return (
    <div className={classes.wrapper}>
      <div className={classes.block}>
        <p className={classes.title}>Компенсация денежных средств</p>
        <div className={classes.container}>
          <Link to="/bank/statement">
            <div className={classes.item}>
              <p className={classes.name}>
                Компенсация при оплате работником <span>Банка франшизы</span>
              </p>
              <SubmitButton className={classes.btn} />
            </div>
          </Link>
          <div className={classes.item}>
            <p className={classes.name}>
              Компенсация при оплате <span>медицинских услуг</span>
            </p>
            <SubmitButton className={classes.btn} />
          </div>
          <div className={`${classes.item} ${classes.item3}`}>
            <p className={classes.name}>
              Компенсация при оплате{" "}
              <span>медицинских услуг и Банка франшизы</span>
            </p>
            <SubmitButton className={classes.btn} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SelectBlock;
