import { useDispatch, useSelector } from "react-redux";
import DownloadButton from "../DownloadButton/DownloadButton";
import RadioButtons from "../RadioButtons/RadioButtons";
import classes from "./PaymentCard.module.css";
import BorderButton from "../BorderButton/BorderButton";
import { useRef, useState } from "react";
import { renameFile, renameFileStatement } from "../../utils/converter";
import { uploadFile } from "../../redux/slices/fileSlice";
import { setCheck, setStatement } from "../../redux/slices/nameSlice";
import success from "../../assets/success.png";
import { setFreeze } from "../../redux/slices/radioSlice";
import { TailSpin } from "react-loader-spinner";
import CheckController from "../CheckController/CheckController";

const PaymentCard = ({ obj }) => {
  const dispatch = useDispatch();
  const selected = useSelector((state) => state.radio.selectedOption);
  const check = useSelector((state) => state.name.check);
  const statement = useSelector((state) => state.name.statement);
  const { uploadStatus, uploadError } = useSelector((state) => state.file);
  const checkInputRef = useRef(null);
  const statementInputRef = useRef(null);
  const choice = useRef("");
  // const [nameCheck, setNameCheck] = useState("");
  // const [nameStatement, setNameStatement] = useState("");
  const [components, setComponents] = useState([]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      let newFile;
      if (choice.current === "check") {
        newFile = renameFile(file, obj.title);
        dispatch(setCheck({ download: true, name: file.name }));
      } else {
        newFile = renameFileStatement(file);
        dispatch(setStatement({ download: true, name: file.name }));
      }

      dispatch(uploadFile(newFile));
      dispatch(setFreeze(true));
    }
  };

  const handleUploadCheckClick = () => {
    choice.current = "check";
    checkInputRef.current.click();
  };

  const handleUploadStatementClick = () => {
    choice.current = "statement";
    statementInputRef.current.click();
  };

  const handleClickMore = () => {
    setComponents([
      ...components,
      <CheckController key={components.length} title={obj.title} />,
    ]);
  };

  console.log("render PaymentCard");
  return (
    <div className={classes.wrapper}>
      <p className={classes.title}>{obj.title}</p>
      <p className={classes.subTitle}>{obj.subTitle}</p>
      <div className={classes.controller}>
        <p className={classes.question}>Как производилась оплата?</p>
        <RadioButtons />
        {selected === "cash" && (
          <div>
            <input
              type="file"
              onChange={handleFileChange}
              style={{ display: "none" }}
              ref={checkInputRef}
            />
            {!check.download && (
              <DownloadButton
                onClick={handleUploadCheckClick}
                text={"Загрузите чек"}
                style={{ padding: "10px 45px", fontSize: "20px" }}
              />
            )}
            {uploadStatus === "succeeded" && check.download && (
              <div className={classes.requestBlock}>
                <img src={success} />
                <p>{check.name}</p>
              </div>
            )}
            {/* {uploadStatus === "loading" && (
              <div className={classes.requestBlock}>
                <TailSpin color="#148F2B" height={55} width={55} />
              </div>
            )} */}
          </div>
        )}
        {selected === "nonCash" && (
          <div className={classes.btn}>
            <input
              type="file"
              onChange={handleFileChange}
              style={{ display: "none" }}
              ref={checkInputRef}
            />
            {!check.download && (
              <DownloadButton
                onClick={handleUploadCheckClick}
                text={"Загрузите чек"}
                style={{
                  padding: "10px 45px",
                  fontSize: "20px",
                }}
                freeze={!statement.download}
              />
            )}
            {uploadStatus === "succeeded" && check.download && (
              <div className={classes.requestBlock}>
                <img src={success} />
                <p>{check.name}</p>
              </div>
            )}
            {/* {uploadStatus === "loading" && !check.download && (
              <div className={classes.requestBlock}>
                <TailSpin color="#148F2B" height={55} width={55} />
              </div>
            )} */}
            <input
              type="file"
              onChange={handleFileChange}
              style={{ display: "none" }}
              ref={statementInputRef}
            />
            {!statement.download && (
              <DownloadButton
                onClick={handleUploadStatementClick}
                text={"Загрузите выписку"}
                style={{ padding: "10px 45px", fontSize: "20px" }}
              />
            )}
            {uploadStatus === "succeeded" && statement.download && (
              <div className={classes.requestBlock}>
                <img src={success} />
                <p>{statement.name}</p>
              </div>
            )}
            {/* {uploadStatus === "loading" && (
              <div className={classes.requestBlock}>
                <TailSpin color="#148F2B" height={55} width={55} />
              </div>
            )} */}
          </div>
        )}
        {components}
      </div>
      <div className={classes.downBlock}>
        {selected === "cash" &&
          check.download &&
          uploadStatus === "succeeded" && (
            <div onClick={handleClickMore}>
              <p>Button</p>
            </div>
          )}
        {selected === "nonCash" &&
          check.download &&
          statement.download &&
          uploadStatus === "succeeded" && (
            <div onClick={handleClickMore}>
              <p>Button</p>
            </div>
          )}
        <BorderButton
          path={obj.path}
          style={{ marginLeft: "auto", marginRight: "50px" }}
        />
      </div>
    </div>
  );
};

export default PaymentCard;
