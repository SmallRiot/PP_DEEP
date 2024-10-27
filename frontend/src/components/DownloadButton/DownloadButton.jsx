import classes from "./DownloadButton.module.css";

const DownloadButton = ({ style }) => {
  return (
    <div className={classes.btn} style={style}>
      <p>Загрузить</p>
    </div>
  );
};

export default DownloadButton;
