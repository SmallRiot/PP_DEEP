import { downloadFile } from "../../redux/slices/fileSlice";
import BorderButton from "../BorderButton/BorderButton";
import { useSelector, useDispatch } from "react-redux";
import classes from "./DownloadPage.module.css";
import { useEffect } from "react";

const DownloadPage = () => {
  const dispatch = useDispatch();
  const { downloadData, downloadStatus, downloadError } = useSelector(
    (state) => state.file
  );

  const handleDownload = () => {
    console.log("click");
    dispatch(downloadFile("12"));
    console.log("post click");
  };

  useEffect(() => {
    if (downloadData) {
      console.log("download");
      const url = window.URL.createObjectURL(new Blob([downloadData]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "document.pdf"); // Укажите имя файла
      document.body.appendChild(link);
      link.click();
      link.remove();
    }
  }, [downloadData]);

  return (
    <div className={classes.wrapper}>
      <div className={classes.title}>
        <p>Результаты проверки</p>
      </div>

      <div className={classes.card}>
        <div>
          <div>Согласен на удаление перс данных </div>
          <div
            className={classes.btn}
            onClick={handleDownload}
            style={{ margin: "auto" }}
          >
            <p>Скачать</p>
          </div>
        </div>
      </div>

      <button onClick={handleDownload}>Download</button>
    </div>
  );
};

export default DownloadPage;
