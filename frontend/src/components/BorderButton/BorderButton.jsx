import classes from "./BorderButton.module.css";

const BorderButton = ({ style }) => {
  return (
    <div className={classes.btn} style={style}>
      <div className={classes.content}>
        <p>Далее</p>
        <p>→</p>
      </div>
    </div>
  );
};

export default BorderButton;
