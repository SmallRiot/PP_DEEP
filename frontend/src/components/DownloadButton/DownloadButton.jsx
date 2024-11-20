import classes from "./DownloadButton.module.css";

const DownloadButton = ({ style, text, onClick }) => {
  return (
    <div onClick={onClick} className={classes.btn} style={style}>
      <p>{text}</p>
    </div>
  );
};

export default DownloadButton;
