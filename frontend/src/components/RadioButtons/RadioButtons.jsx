import classes from "./RadioButtons.module.css";
import { useSelector, useDispatch } from "react-redux";
import { selectOption } from "../../redux/slices/radioSlice";

const RadioButtons = () => {
  const dispatch = useDispatch();
  const selected = useSelector((state) => state.radio.selectedOption);
  const freeze = useSelector((state) => state.radio.freeze);

  console.log(selected);
  return (
    <div className={classes.block}>
      <div className={classes.radioBtn}>
        <p>Наличными</p>
        <div
          className={classes.dot}
          onClick={() => {
            if (!freeze) {
              dispatch(selectOption("cash"));
            }
          }}
        >
          <span
            className={`${classes.down} ${
              selected === "cash" ? classes.downActive : ""
            }`}
          ></span>
          <span
            className={`${classes.up} ${
              selected === "cash" ? classes.upActive : ""
            }`}
          ></span>
        </div>
      </div>
      <div className={classes.radioBtn}>
        <p>Безналичный расчет</p>
        <div
          className={classes.dot}
          onClick={() => {
            if (!freeze) {
              dispatch(selectOption("nonCash"));
            }
          }}
        >
          <span
            className={`${classes.down} ${
              selected === "nonCash" ? classes.downActive : ""
            }`}
          ></span>
          <span
            className={`${classes.up} ${
              selected === "nonCash" ? classes.upActive : ""
            }`}
          ></span>
        </div>
      </div>
    </div>
  );
};

export default RadioButtons;
