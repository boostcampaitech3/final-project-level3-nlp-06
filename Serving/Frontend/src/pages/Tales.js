import { Chip, Typography, Alert } from "@material-tailwind/react";
import axios from "axios";
import { debounce } from "lodash";
import React, { useEffect, useState } from "react";
import { SpinnerCircular } from "spinners-react";
import DefaultFooter from "../components/Footer";
import Navibar from "../components/Navibar";
import TaleCard from "../components/Talecard";

const Tales = (props) => {
  //const currentPage = props.pageNum;
  const [currentPage, setCurrentPage] = useState(0);
  const [talesNum, setTalesNum] = useState(6);

  const [pageCount, setPageCount] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [pageNum, setPageNum] = useState(0);

  const [loading, setLoading] = useState(false);
  const [serverState, setServerState] = useState(true);

  // tales 에는 {'id', 'title', 'author', 'text', 'imge'}가 있음
  const [tale, setTale] = useState({
    id: "",
    title: "",
    author: "",
    text: "",
    image: "",
  });
  const [tales, setTales] = useState([]);

  const getTalesCount = async (e) => {
    const response = await axios
      .get(`${process.env.REACT_APP_SERVER_ADDRESS}/tales`, { timeout: 10000 })
      .then((res) => {
        if (res) {
          // rest.data 에는 전체 개수가 옵니다.
          console.log(`res is ${res.data}`);
          // 페이지 개수는 전체/talesNum 입니다.
          setTotalCount(res.data);
          setPageCount(Math.floor(res.data / talesNum) + 1);
          setServerState(true);
        }
      })
      .catch((err) => {
        alert(
          err + "\n현재 서버가 중지된 상태입니다. 관리자에게 문의해주세요!"
        );
      });
  };

  // 현재 page number에 해당하는 tale들을 가져옵니다.
  const getTales = async (pageNum) => {
    // 먼저 6개의 쿼리를 가져옵니다.
    // 역순으로 가져와야겠지..?
    //const talesNum = totalCount;

    console.log(`get ${talesNum}개 tale `);
    console.log(currentPage, " 번째 페이지 접근중");

    // 이전 tales를 비워줍니다
    setTales([]);

    // 페이지 넘버에 맞는 tales를 가져옵니다.

    // 0; idx <= talesNum
    for (
      let idx = currentPage * talesNum + 1;
      idx <= currentPage * talesNum + talesNum;
      idx++
    ) {
      await axios
        .get(`${process.env.REACT_APP_SERVER_ADDRESS}/tales/${idx}`, {
          timeout: 10000,
        })
        .then((res) => {
          // res 에는 데이터가 옵니다..
          if (res.data.message) {
            // message는 오류임 (없다는 뜻)
            return;
          } else {
            console.log(`getTales [res] is ${res.data.message}`);
            console.log(res.data);

            const inputForm = {
              id: idx,
              title: res.data.title,
              author: res.data.author,
              text: res.data.text,
              imgbs64: res.data.chg_img_bs64,
            };
            console.log(inputForm);

            setTales((tales) => [...tales, inputForm]);
            setLoading(true);
          }
        })
        .catch((err) => {
          //alert(err);
        });
      //break;
    }
  };

  // page 클릭에 따라서 해당되는 쿼리를 돌립니다.
  const onPageClick = (e) => {
    console.log(e.target.innerText);
    setCurrentPage(e.target.innerText - 1);
  };

  useEffect(() => {
    console.log("useEffect");

    // 서버에서 count를 가져옵니다
    getTalesCount();
    // 서버에서 페이지에 해당하는 tale들을 가져옵니다.
    //getTales();

    // 페이지네이션

    // setTotalCount 비동기 처리
  }, [totalCount, serverState]);

  useEffect(() => {
    getTales();
  }, [currentPage, talesNum]);

  const onTest = (e) => {
    console.log(tales);
    console.log(pageCount);
  };
  //bg-gradient-to-t from-myBlue to-myGreen
  return (
    <>
      <div className=""></div>
      <div className="tales-bg bg-gradient-to-tr bg-myBlue from-myBluex to-myYellowx">
        <Navibar />
        <div className="max-w-screen-xlt pb-20 px-4 lg:px-20">
          {loading ? (
            <main className="">
              <div className="relative pt-16 pb-32x flex flex-col items-center justify-center">
                <div className="font-dungen text-center border-4 bg-opacity-70 text-white bg-light-blue-400 px-12 py-4 rounded-2xl text-6xl">
                  담벼락
                </div>
                <button className="invisible" onClick={onTest}>
                  Test Button
                </button>
                {totalCount ? (
                  <p className="pb-4 text-white font-dungen">
                    현재 총 {totalCount}건의 글이 있습니다!
                  </p>
                ) : (
                  "아직 아무것도 없네요!"
                )}
                <Chip value="PAGE" />
                <div className="flex pb-8 flex-row gap-4 text-blue-400">
                  {pageCount
                    ? [...Array(pageCount)].map((_, idx) => (
                        <div
                          className="cursor-pointer text-2xl hover:text-green-600 hover:scale-150 duration-200"
                          onClick={onPageClick}
                        >
                          {idx + 1}
                        </div>
                      ))
                    : "none"}
                </div>
              </div>
              <div className="flex flex-row flex-wrap items-center justify-center gap-12 px-">
                {tales
                  ? tales.map((tale) => (
                      <TaleCard
                        id={tale.id}
                        title={tale.title}
                        author={tale.author}
                        text={tale.text}
                        imgbs64={tale.imgbs64 ? tale.imgbs64 : ""}
                      />
                    ))
                  : "NONE"}
              </div>
              <div className="py-8 flex flex-col items-center justify-center"></div>
            </main>
          ) : (
            <main>
              <div className="relative h-screen pt-16 pb-32 flex items-center justify-center">
                <SpinnerCircular size={150} enabled={true} />
              </div>
            </main>
          )}
        </div>
      </div>
      <DefaultFooter />
    </>
  );
};

export default Tales;

// "py-8 flex flex-row flex-wrap gap-4 items-center justify-center"
// <Typography color="light-blue" variant="h1" className="py-12">
// 구경 하기!
// </Typography>
