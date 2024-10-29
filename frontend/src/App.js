import "./App.css";
import Header from "./components/Header/Header";
import Start from "./components/Start/Start";
import BankPage from "./components/BankPage/BankPage";
import { Route, Routes } from "react-router-dom";
import Card from "./components/Card/Card";
import PaymentCard from "./components/PaymentCard/PaymentCard";

function App() {
  const arr = [
    {
      title: "Заявление",
      subTitle:
        "Копия Заявление о мед услугах и тд тп тд аывыгаовышавышаугкаркнгырмсвымиваимавымваирмавыор",
      path: "certificate",
      initPath: "statement",
    },
    {
      title: "Свидетельство о рождении",
      subTitle:
        "Копия свидетельства о рождении ребенка или копия документа, подтверждающего усыновление/ удочерение/опекунство/попечительство",
      path: "marriage-certificate",
      initPath: "certificate",
    },
    {
      title: "Свидетельство о браке",
      subTitle:
        "предоставляется, если расходы понесены родителем ребенка – не работником Банка",
      path: "agreement",
      initPath: "marriage-certificate",
    },
    {
      title: "Согласие на обработку персональных данных ",
      subTitle:
        "Письменное согласие на обработку персональных данных работника Банка в целях получения компенсации за медицинское обслуживание несовершеннолетнего ребенка",
      path: "agreement-minor",
      initPath: "agreement",
    },
    {
      title: "Согласие на обработку персональных данных несовершеннолетнего",
      subTitle:
        "Письменное согласие на обработку персональных данных несовершеннолетнего в целях получения компенсации работником Банка за медицинское обслуживание ребенка, заполняемое уполномоченным представителем несовершеннолетнего",
      path: "contract",
      initPath: "agreement-minor",
    },
    {
      title: "Копия договора об оказании медицинских услуг",
      subTitle:
        "Нету инфы, но что-то нужно вставить сюда 100%% аываывагше56ке3278врфыпангвап63пануагпвыфнапвыгфанпы",
      path: "gg",
      initPath: "contract",
    },
  ];
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="" element={<Start />} />
        <Route path="/bank" element={<BankPage />}>
          {arr.map((el) => {
            return <Route path={el.initPath} element={<Card obj={el} />} />;
          })}
          {/* <Route path="" element={<Card />} />
          <Route path="certificate" element={<Card />} /> */}
          <Route
            path="gg"
            element={
              <PaymentCard
                obj={{
                  title: "Кассовый чек",
                  subTitle:
                    "Нету инфы, но что-то нужно вставить сюда 100%% аываывагше56ке3278врфыпангвап63пануагпвыфнапвыгфанпы",
                  path: "gg",
                  initPath: "contract",
                }}
              />
            }
          />
        </Route>
        {/* <Start /> */}
      </Routes>
    </div>
  );
}

export default App;
