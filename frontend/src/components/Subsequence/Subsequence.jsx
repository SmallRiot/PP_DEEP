import Cell from "../Cell/Cell";
import Separator from "../Separator/Separator";
import classes from "./Subsequence.module.css";

const Subsequence = ({ count }) => {
  return (
    <div className={classes.block}>
      {Array(count)
        .fill()
        .map((_, i) => {
          if (i + 1 == count) {
            return <Cell number={i + 1} />;
          } else {
            return (
              <div className={classes.cell}>
                <Cell number={i + 1} />
                <Separator />
              </div>
            );
          }
        })}
    </div>
  );
};

export default Subsequence;
