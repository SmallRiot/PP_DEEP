import { useState } from "react";
import classes from "./RadioButtons.module.css";

const RadioButtons = () => {
  const [selected, setSelected] = useState("");

  const handleClick = (option) => {
    if (option !== selected) {
      setSelected(option);
    }
  };

  return (
    <div className={classes.block}>
      <div className={classes.radioBtn}>
        <p>Наличными</p>
        <div className={classes.dot} onClick={() => handleClick("selected1")}>
          <span
            className={`${classes.down} ${
              selected === "selected1" ? classes.downActive : ""
            }`}
          ></span>
          <span
            className={`${classes.up} ${
              selected === "selected1" ? classes.upActive : ""
            }`}
          ></span>
        </div>
      </div>
      <div className={classes.radioBtn}>
        <p>Безналичный расчет</p>
        <div className={classes.dot} onClick={() => handleClick("selected2")}>
          <span
            className={`${classes.down} ${
              selected === "selected2" ? classes.downActive : ""
            }`}
          ></span>
          <span
            className={`${classes.up} ${
              selected === "selected2" ? classes.upActive : ""
            }`}
          ></span>
        </div>
      </div>
    </div>
  );
};

export default RadioButtons;
