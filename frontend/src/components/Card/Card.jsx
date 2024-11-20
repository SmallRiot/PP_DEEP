import { useRef } from "react";
import BorderButton from "../BorderButton/BorderButton";
import DownloadButton from "../DownloadButton/DownloadButton";
import { useSelector, useDispatch } from "react-redux";
import classes from "./Card.module.css";
import { uploadFile } from "../../redux/slices/fileSlice";
import success from "../../assets/success.png";
import errorImg from "../../assets/errorImg.png";
import { initFile } from "../../redux/slices/fileSlice";

const Card = ({ obj }) => {
  const dispatch = useDispatch();
  const { uploadStatus, error } = useSelector((state) => state.file);

  const handleFileChange = (event) => {
    console.log(event.target.files[0]);
    console.log("Pre-Send");
    dispatch(uploadFile(event.target.files[0]));
    console.log("Send");
    console.log(event.target.files[0]);
  };
  const fileInputRef = useRef(null);
  const handleUploadClick = () => {
    console.log("click");
    fileInputRef.current.click();
  };

  return (
    <div className={classes.wrapper}>
      <p className={classes.title}>{obj.title}</p>
      <p className={classes.subTitle}>{obj.subTitle}</p>
      <input
        type="file"
        onChange={handleFileChange}
        style={{ display: "none" }}
        ref={fileInputRef}
      />
      {uploadStatus === "idle" && (
        <DownloadButton
          onClick={handleUploadClick}
          style={{ alignSelf: "center" }}
          text={"Загрузить"}
        />
      )}
      {uploadStatus === "loading" && <p>Идет загрузка файла</p>}
      {uploadStatus === "succeeded" && (
        <div className={classes.requestBlock}>
          <img src={success} />
        </div>
      )}
      {uploadStatus === "failed" && (
        <div className={classes.requestBlock}>
          <img src={errorImg} />
          <p>{error}</p>
        </div>
      )}
      <div className={classes.downBlock}>
        {/* <div>
          <p>Документ заполнен верно</p>
        </div> */}
        <BorderButton
          onClick={() => dispatch(initFile())}
          path={obj.path}
          style={{ marginLeft: "auto" }}
        />
      </div>
    </div>
  );
};

export default Card;
