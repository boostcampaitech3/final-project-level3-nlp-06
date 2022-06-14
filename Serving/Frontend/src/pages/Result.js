import React from "react";
import { useLocation, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import Navibar from "../components/Navibar";
import {
  Button,
  Popover,
  PopoverContent,
  PopoverHandler,
  Typography,
} from "@material-tailwind/react";
//import { SERVER_ADDRESS } from "../constants";
import DefaultFooter from "../components/Footer";
import KakaoShareButton from "../components/KakaoShare";

const Result = () => {
  const location = useLocation();
  //console.log("location!");
  //console.log(location.state);

  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [resultText, setResultText] = useState("");
  const [styledImage, setStyledImage] = useState(null);
  const [ind, setInd] = useState();

  // 만약 제출 없이 그냥 result 페이지로 접속하는 경우 에러가 발생함!

  useEffect(() => {
    if (!location.state) {
      alert("잘못된 접근!");
      return;
    }
    console.log("useEff");
    console.log(location.state);
    setTitle(location.state.res.title);
    setAuthor(location.state.res.author);
    setResultText(location.state.result_text);
    setStyledImage(location.state.res.chg_file_bs64); // chg_img_url
    setInd(location.state.res.ind);
    //setStyledImage(URL.createObjectURL(location.state.res.styledImage));
  }, []);

  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://developers.kakao.com/sdk/js/kakao.js";
    script.async = true;

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  console.log(ind);
  console.log(location.state);
  console.log(`${styledImage}`);

  // 버튼을 누르면 link를 복사합니다.
  const onCopyClick = async (e) => {
    // 링크를 클립보드로 복사합니다.
    // copy -> .../tales/ind
    let link = window.location.href.split("/result")[0];
    link = link + `/tales/${ind}`;
    console.log(link);
    navigator.clipboard.writeText(link);
  };

  return (
    <>
      <div className=""></div>
      <main className="write-bg">
        <Navibar />
        <div className="relative pt-16 pb-32 flex flex-col content-center items-center justify-center xh-screen">
          <div className="w-fullx lg:w-6/12 px-6 py-12 text-center bg-white bg-opacity-70 rounded-3xl">
            <div>
              {title ? (
                <Typography
                  className="pb-12"
                  variant="h1"
                  color="light-blue"
                  textGradient
                >
                  {title}
                </Typography>
              ) : (
                "title not found"
              )}
              <div className="flex flex-col justify-center items-center gap-10">
                {author ? (
                  <Typography variant="h5">{author}</Typography>
                ) : (
                  "author not found "
                )}
                {resultText ? (
                  <Typography
                    className="border-2 border-dotted rounded-lg px-2 py-2 border-blue-grey-300"
                    variant="paragraph"
                  >
                    {resultText}
                  </Typography>
                ) : (
                  "text not found "
                )}
                {styledImage ? (
                  <img
                    alt="img here"
                    src={`data:imgae/png;base64,${styledImage}`}
                    height="360"
                    width="360"
                  />
                ) : (
                  "no image"
                )}
              </div>
            </div>
          </div>
          <div>
            <Popover>
              <PopoverHandler onClick={onCopyClick}>
                <Button size="lg">링크복사</Button>
              </PopoverHandler>
              <PopoverContent>링크 복사 완료!</PopoverContent>
            </Popover>
          </div>
          <KakaoShareButton />
        </div>
      </main>
      <DefaultFooter />
    </>
  );
};

export default Result;
