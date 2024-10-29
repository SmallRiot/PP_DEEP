import RadioButtons from "../RadioButtons/RadioButtons";
import classes from "./PaymentCard.module.css";

const PaymentCard = ({ obj }) => {
  return (
    <div className={classes.wrapper}>
      <p className={classes.title}>{obj.title}</p>
      <p className={classes.subTitle}>{obj.subTitle}</p>
      <div className={classes.controller}>
        <p className={classes.question}>Как производилась оплата?</p>
        <RadioButtons />
      </div>
    </div>
  );
};

export default PaymentCard;
