import { useLocation } from "react-router-dom";
import Cell from "../Cell/Cell";
import Separator from "../Separator/Separator";
import classes from "./Subsequence.module.css";

const Subsequence = ({ count }) => {
  const location = useLocation();
  /* ReduxToolkit Хранить массив, как в arr и сравнивать текущий путь с initPath и изменять ячейку*/
  const currentPath = location.pathname.slice(1);
  const arr = currentPath.split("/");
  const chapter = arr[arr.length - 1];
  return (
    <div className={classes.block}>
      {Array(count)
        .fill()
        .map((_, i) => {
          if (i + 1 === count) {
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
