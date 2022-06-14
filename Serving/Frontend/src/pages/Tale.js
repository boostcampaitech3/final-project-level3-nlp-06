import { Typography } from "@material-tailwind/react";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import DefaultFooter from "../components/Footer";
import Navibar from "../components/Navibar";

const Tale = (props) => {
  const param = useParams();
  const [tale, setTale] = useState("");

  console.log(param);

  const getTale = async (e) => {
    await axios
      .get(`${process.env.REACT_APP_SERVER_ADDRESS}/tales/${param.id}`, {
        timeout: 10000,
      })
      .then((res) => {
        // res 에는 데이터가 옵니다..
        if (res.data.message) {
          // message는 오류임 (없다는 뜻)
          return;
        } else {
          const inputForm = {
            id: param.id,
            title: res.data.title,
            author: res.data.author,
            text: res.data.text,
            imgbs64: res.data.chg_img_bs64,
          };
          console.log(inputForm);

          //setTales((tales) => [...tales, inputForm]);
          setTale(inputForm);
          //setLoading(true);
        }
      })
      .catch((err) => {
        //alert(err);
      });
  };

  useEffect(() => {
    getTale();
  }, []);

  //const { state } = useLocation();
  //console.log(state);
  //console.log(state.id);

  return (
    <>
      <div className=""></div>
      <main className="write-bg">
        <Navibar />
        <div className="relative pt-16 pb-32 flex content-center items-center justify-center xh-screen">
          <div className="w-fullx lg:w-6/12 px-6 py-12 text-center bg-white bg-opacity-70 rounded-3xl">
            <div>
              {tale.title ? (
                <Typography
                  className="pb-12"
                  variant="h1"
                  color="light-blue"
                  textGradient
                >
                  {tale.title}
                </Typography>
              ) : (
                "no"
              )}
            </div>
            <div className="flex flex-col gap-10 justify-center items-center">
              {tale.author ? (
                <Typography variant="h5">{tale.author}</Typography>
              ) : (
                "no"
              )}
              {tale.text ? (
                <Typography
                  className="border-2 border-dotted rounded-lg px-2 py-2 border-blue-grey-300"
                  variant="paragraph"
                >
                  {tale.text}
                </Typography>
              ) : (
                "nooo"
              )}

              {tale.imgbs64 ? (
                <img
                  src={`data:image/png;base64,${tale.imgbs64}`}
                  alt="img-blur-shadow"
                  height="360"
                  width="360"
                />
              ) : (
                "no image"
              )}
            </div>
          </div>
        </div>
      </main>

      <DefaultFooter />
    </>
  );
};

export default Tale;
