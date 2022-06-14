import React from "react";
import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router";

import axios from "axios";
import Slider from "rc-slider";
import "rc-slider/assets/index.css";
import Navibar from "../components/Navibar";
import {
  Alert,
  Checkbox,
  Chip,
  Input,
  Textarea,
  Tooltip,
  Typography,
} from "@material-tailwind/react";
import DefaultFooter from "../components/Footer";
import {
  Button,
  Modal,
  Form,
  FormControl,
  FormGroup,
  FormLabel,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
} from "react-bootstrap";

const Write = () => {
  const navigate = useNavigate();
  const [serverPing, setServerPing] = useState(false);

  const [text, setText] = useState("");
  const [result, setResult] = useState(" ");
  //const [title, setTitle] = useState("제목 없음");
  //const [author, setAuthor] = useState("익명");
  const [isPredLoading, setIsPredLoading] = useState(true);
  const submitRef = useRef();

  const [useAPI, setUseAPI] = useState(false);

  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const [maxLen, setMaxLen] = useState(2);
  const [temperature, setTemperature] = useState(0.85);
  const [repetPenalty, setRepetPenalty] = useState(1.5);

  const [proposalList, setProposalList] = useState([]);

  const [imgFile, setImgFile] = useState(null);
  const [imgFileData, setImgFileData] = useState(null);
  const [imgBase64, setImgBase64] = useState([]); // base64 encoding
  const imgInputRef = useRef();

  const onChange = (e) => {
    setText(e.target.value); //
    //setResult(result.concat(e.target.value)); // textarea
  };
  const onChangeTA = (e) => {
    setResult(e.target.value);
  };

  // loading
  useEffect(() => {
    autoResizeTA();
  }, [isPredLoading, result, proposalList]);
  useEffect(() => {
    onPingPong();
  }, []);

  // 맞춤법 교정 사용 여부
  const checkHandler = (e) => {
    setUseAPI(!useAPI);
  };

  // 로딩 핸들러
  const loadingHandler = (e) => {
    //setIsPredLoading(!isPredLoading);
    setIsPredLoading(e);
  };

  // text area 리사이즈
  const autoResizeTA = () => {
    let textarea = document.querySelector(".autoTextarea");
    if (textarea) {
      textarea.style.height = "auto";
      let height = textarea.scrollHeight;
      textarea.style.height = `${height + 8}px`;
    }
  };

  // input 입력 - 서버로 string 전송 후 predict string을 받아옴
  const onKeyPress = async (e) => {
    if (e.key === "Enter") {
      loadingHandler(false);
      if (e.target.value === "") {
        // 빈 입력 방지
        alert("빈 입력은 허용되지 않습니다!");
        return;
      }
      const target = e.target.value;
      setText("");

      // Form data
      const fd = new FormData();
      console.log(`result: ${result}`);
      fd.append("result", result);
      fd.append("data", target);
      fd.append("sentence_count", maxLen);
      fd.append("temperature", temperature);
      fd.append("repetition", repetPenalty);
      fd.append("grammar_check", useAPI);
      console.log(fd);
      console.log(fd.result, target);
      console.log(fd.data, result);
      // POST request //
      const s_t = new Date();
      await axios
        .post(`${process.env.REACT_APP_SERVER_ADDRESS}/predict`, fd, {
          headers: {
            "Content-Type": `stringpart/form-data`,
          },
        })
        .then((res) => {
          if (res.data) {
            // Result Text Area에 들어감
            const proposalForm = [res.data[0], res.data[1], res.data[2]];
            setProposalList(proposalForm);
            //const going = " " + res.data.generate_text;
            //setResult(result.concat(going + " "));
            loadingHandler(true);
            //autoResizeTA();
          }
        })
        .catch((err) => {
          alert(err);
          loadingHandler(true);
        });
      const e_t = new Date();
      console.log(e_t - s_t);
    }
  };

  const onProposalClick = (e) => {
    // TextArea에 들어가게 됩니다.
    const adding = " " + e.target.innerText;
    setResult(result.concat(adding + " "));
    // 리스트 초기화!
    setProposalList([]);
  };

  // image 업로드 -> Base64 encoding -> 브라우저에 띄움
  const onImageUpload = (e) => {
    if (e.target.files[0]) {
      setImgFile(URL.createObjectURL(e.target.files[0]));
      setImgFileData(e.target.files[0]); //imgFile
      setImgBase64([]);
      // base64 encode
      for (var i = 0; i < e.target.files.length; i++) {
        if (e.target.files[i]) {
          let reader = new FileReader();
          reader.readAsDataURL(e.target.files[i]);
          // File load
          reader.onload = () => {
            const base64 = reader.result; // bitmap data return
            //console.log(base64);
            if (base64) {
              var base64Sub = base64.toString();
              // base64 update
              // setImgBase64((imgBase64) => [...imgBase64, base64Sub]);
            }
          };
        }
      }
      //
    }
  };

  const onImageUploadBtnClick = (e) => {
    e.preventDefault();
    console.log("click");
    imgInputRef.current.click();
  };

  // 제출 -> text area & image 서버로 전송
  const handleSubmit = async (e) => {
    console.log(process.env);
    e.preventDefault();
    if (!result) {
      alert("완성된 글이 없습니다!");
      return;
    }

    const fd = new FormData();
    if (imgFile) {
      // Object.values(imgBase64).forEach((file) => fd.append("file", file)); base64
      console.log("imgFile fd 탑재");
      //console.log(imgFileData);
      fd.append("file", imgFileData);
    } else {
      //fd.append("file", null);
    }
    fd.append("text", result);

    // 작가 및 제목 입력창 생성
    //handleShow();
    let title = prompt("제목을 입력해주세요!", "제목없음");
    let author = prompt("작가의 이름은 무엇인가요?", "익명");

    if (!title) {
      title = "제목 없음";
    }
    if (!author) {
      author = "익명";
    }

    fd.append("author", author);
    fd.append("title", title);

    console.log(fd);
    await axios
      .post(`${process.env.REACT_APP_SERVER_ADDRESS}/submit`, fd, {
        headers: {
          "Content-Type": `multipart/form-data;`,
        },
      })
      .then((res) => {
        // page 전환
        // res에는 StyleGAN이 적용된 이미지가 옴
        if (res.data) {
          console.log(res.data);
        }
        navigate("/result", {
          state: {
            result_text: result,
            res: res.data,
          },
        });
      })
      .catch((err) => {
        alert(err);
      });
  };

  const onPingPong = (e) => {
    //e.preventDefault();
    const res = axios
      .get(`${process.env.REACT_APP_SERVER_ADDRESS}/`)
      //.get("http://naver.com")
      .then(function (res) {
        console.log(res);
        //console.log(res.data);
        setServerPing(true);
      })
      .catch(function (error) {
        console.log(error);
        setServerPing(false);
      });
  };

  return (
    <div className="bg-blue-grey-200">
      <main className="write-bg">
        <Navibar />
        <div className="pb-20 px-2 md:px-4 lg:px-20 flex flex-col justify-center items-center">
          <div className="px-12 bg-opacity-70 bg-white rounded-3xl max-w-screen-xl flex-initial mt-20 ">
            <div className="py-4 px-4">
              {serverPing ? (
                <Tooltip content="현재 AI 서버가 작동중입니다.">
                  <Chip color="cyan" value="서버 연결됨" />
                </Tooltip>
              ) : (
                <Tooltip content="현재 AI 서버가 중지된 상태입니다.">
                  <Chip color="red" value="서버 끊어짐" />
                </Tooltip>
              )}
            </div>
            <div className="max-w-screen-md mx-auto py-8 text-wh">
              <div className="text-center py-4">
                <Typography variant="h1" color="brown" className="font-woori">
                  동화 글쓰기
                </Typography>
              </div>
              <p className="text-right">{result.length} / 1024</p>
              <Textarea
                label="Result"
                ref={submitRef}
                value={result}
                onChange={onChangeTA}
                variant="outlined"
                color="teal"
                className="autoTextarea"
                success
              />
            </div>
            <div className="max-w-screen-md mx-auto pb-6">
              <Alert color="brown" className="mb-8">
                문장을 입력하는 경우에는 구두점(. ! ?)을 빼먹지 말아주세요!
              </Alert>
              <Input
                label="글을 써봅시다!"
                onChange={onChange}
                value={text}
                onKeyPress={onKeyPress}
                variant="outlined"
                success
              />
              <Checkbox
                className="border-2 border-blue-400"
                label="맞춤법 교정 사용"
                checked={useAPI}
                onChange={(e) => checkHandler(e)}
              />
              <div className="flex justify-center">
                {isPredLoading ? (
                  <p className="bg-green-700 text-white w-max rounded-lg">
                    🤖대기중🤖
                  </p>
                ) : (
                  <p className="bg-purple-600 text-white w-max rounded-lg">
                    🤖두뇌 풀가동!🤖
                  </p>
                )}
              </div>
              <div className="flex flex-col justify-center gap-4 py-4">
                {proposalList
                  ? proposalList.map((proposal) => (
                      <div>
                        <Alert
                          className="hover:bg-amber-400 hover:text-black"
                          onClick={onProposalClick}
                        >
                          {proposal}
                        </Alert>
                      </div>
                    ))
                  : ""}
              </div>
            </div>
            <div className="max-w-screen-md mx-auto">
              <Tooltip content="AI가 지어낼 문장의 갯수입니다.">
                <p>문장 길이 {maxLen}</p>
              </Tooltip>
              <Slider
                min={1}
                max={5}
                defaultValue={2}
                onChange={(e) => {
                  setMaxLen(e);
                }}
              />
              <Tooltip content="높을수록 AI가 자유롭게 글을 써내려갑니다. 추천:0.85">
                <p>Temperature {temperature}</p>
              </Tooltip>
              <Slider
                min={1}
                max={100}
                defaultValue={85}
                onChange={(e) => {
                  setTemperature(e / 100);
                }}
              />
              <Tooltip content="높을수록 단어의 반복을 방지합니다. 추천:1.5">
                <p>Repetition Penalty {repetPenalty}</p>
              </Tooltip>
              <Slider
                min={10}
                max={20}
                defaultValue={15}
                onChange={(e) => {
                  setRepetPenalty(e / 10);
                }}
              />
            </div>
            <form onSubmit={handleSubmit}>
              <div className="max-w-screen-md mx-auto content-evenly px-10 py-10 flex flex-row space-x-12">
                {imgFile === "" ? (
                  <p className="text-red-800">no image</p>
                ) : (
                  <img
                    className="h-28 transition-all duration-300 md:h-40 lg:h-40"
                    alt=""
                    src={imgFile}
                  />
                )}
                <div>
                  <input
                    ref={imgInputRef}
                    type="file"
                    id="uploadImg"
                    accept="image/*"
                    name="file"
                    onChange={onImageUpload}
                    style={{ display: "none" }}
                  />
                </div>
              </div>
              <div className="py-8 gap-4 flex flex-col sm:flex-row">
                <Tooltip content="이미지를 올리면 동화풍으로 바꿔줍니다.">
                  <button
                    className="py-2 px-2 rounded-lg shadow-md text-white bg-blue-500 hover:bg-blue-800"
                    onClick={onImageUploadBtnClick}
                  >
                    사진 업로드
                  </button>
                </Tooltip>
                <button
                  className="py-2 px-2 rounded-lg shadow-md text-white bg-blue-500 hover:bg-blue-800"
                  type="submit"
                >
                  완성! 제출!
                </button>
              </div>
            </form>
          </div>
        </div>
        <DefaultFooter />
      </main>
    </div>
  );
};

export default Write;
