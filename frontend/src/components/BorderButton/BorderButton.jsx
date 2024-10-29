import { Link } from "react-router-dom";
import classes from "./BorderButton.module.css";

const BorderButton = ({ style, path }) => {
  return (
    <Link to={`/bank/${path}`} className={classes.btn} style={style}>
      <div className={classes.content}>
        <p>Далее</p>
        <p>→</p>
      </div>
    </Link>
  );
};

export default BorderButton;
