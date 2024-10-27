import BorderButton from "../BorderButton/BorderButton";
import DownloadButton from "../DownloadButton/DownloadButton";
import classes from "./Card.module.css";

const Card = () => {
  return (
    <div className={classes.wrapper}>
      <p className={classes.title}>Свидетельство о рождении</p>
      <p className={classes.subTitle}>
        Копия свидетельства о рождении ребенка или копия документа,
        подтверждающего усыновление/ удочерение/опекунство/попечительство{" "}
      </p>
      <DownloadButton style={{ alignSelf: "center" }} />
      <BorderButton
        style={{ alignSelf: "end", marginRight: "50px", marginTop: "110px" }}
      />
    </div>
  );
};

export default Card;
