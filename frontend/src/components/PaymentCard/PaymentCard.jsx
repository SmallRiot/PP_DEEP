import { useSelector } from "react-redux";
import DownloadButton from "../DownloadButton/DownloadButton";
import RadioButtons from "../RadioButtons/RadioButtons";
import classes from "./PaymentCard.module.css";
import BorderButton from "../BorderButton/BorderButton";

const PaymentCard = ({ obj }) => {
  const selected = useSelector((state) => state.radio.selectedOption);
  console.log("render");
  return (
    <div className={classes.wrapper}>
      <p className={classes.title}>{obj.title}</p>
      <p className={classes.subTitle}>{obj.subTitle}</p>
      <div className={classes.controller}>
        <p className={classes.question}>Как производилась оплата?</p>
        <RadioButtons />
        {selected === "cash" && (
          <DownloadButton
            text={"Загрузите чек"}
            style={{ padding: "10px 45px", fontSize: "20px" }}
          />
        )}
        {selected === "nonCash" && (
          <div className={classes.btn}>
            <DownloadButton
              text={"Загрузите чек"}
              style={{ padding: "10px 45px", fontSize: "20px" }}
            />
            <DownloadButton
              text={"Загрузите выписку"}
              style={{ padding: "10px 45px", fontSize: "20px" }}
            />
          </div>
        )}
      </div>
      <BorderButton style={{ alignSelf: "end", marginRight: "50px" }} />
    </div>
  );
};

export default PaymentCard;
