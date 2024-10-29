import BorderButton from "../BorderButton/BorderButton";
import DownloadButton from "../DownloadButton/DownloadButton";
import classes from "./Card.module.css";

const Card = ({ obj }) => {
  return (
    <div className={classes.wrapper}>
      <p className={classes.title}>{obj.title}</p>
      <p className={classes.subTitle}>{obj.subTitle}</p>
      <DownloadButton style={{ alignSelf: "center" }} />
      <BorderButton
        path={obj.path}
        style={{ alignSelf: "end", marginRight: "50px", marginTop: "110px" }}
      />
    </div>
  );
};

export default Card;
