import { faArrowUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Typography } from "@material-tailwind/react";
import React from "react";
import { Link } from "react-router-dom";
import DefaultFooter from "../components/Footer";
import Navibar from "../components/Navibar";
import TaleCard from "../components/Talecard";
import { examples } from "../constants";

const Home = () => {
  return (
    <>
      <main className="">
        <div className=""></div>
        <section class="title-bg" id="title">
          <div className="relative pt-16 pb-32 flex content-center items-center justify-center">
            <div className="container max-w-8xl relative amx-auto">
              <Navibar />
              <div className="items-center flex flex-wrap pt-12 px-12 justify-center">
                <div>
                  <img
                    className="max-h-fit max-w-sm lg:max-w-md transition-all"
                    src="./image1.png"
                    alt=""
                  />
                </div>
                <div className="w-full lg:w-6/12 px-4 pt-20 ml-auto mr-auto text-center transition-all">
                  <h1 className="headText">Welcome</h1>
                  <h1 className="headline">Your story starts with us.</h1>
                  <h5 className="headline-description">Ready to be open</h5>
                </div>
              </div>
            </div>
          </div>
        </section>
        {/* Headline end */}
        {/* Storyline start */}
        <section className="discover-out-story flex justify-center">
          <div className="container">
            <div className="project-info">
              <div className="project-description padding-right animate-left">
                <div className="global-headline">
                  <h1 className="headText">Discover</h1>
                  <h1 className="headline headline-dark">Our Project</h1>
                </div>
                <p>
                  이 프로젝트에서는 GPT-3와 StyleGAN을 이용하여 동화를
                  생성합니다.
                </p>
                <Link to="/about" class="body-btn">
                  더 알아보기
                </Link>
              </div>
              <div className="flex justify-center project-info-img animate-right pb-8">
                <img alt="" src="./image3.png" />
              </div>
            </div>
          </div>
        </section>
        {/* Storyline end */}
        {/* Card section start */}
        <section class="story-examples between">
          <div className="container mx-auto py-4 lg:py-10">
            <div className="project-info">
              <div className="project-description padding-right animate-left">
                <div className="global-headline">
                  <div className="animate-top">
                    <h1 className="headText">Check</h1>
                  </div>
                  <div className="animate-bottom">
                    <h1 className="headline">Story Sample</h1>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="flex justify-center pb-10">
            <a href="#title" class="bottom-btn">
              <FontAwesomeIcon
                icon={faArrowUp}
                size="2x"
                className="hover:animate-bounce"
              />
            </a>
          </div>
          <div className="py-20 px-20 flex xl:flex-row items-center justify-center transition-all gap-8 flex-col">
            {examples.map((exam) => (
              <TaleCard
                id={exam.id}
                title={exam.title}
                author={exam.author}
                text={exam.text}
                imgbs64={exam.imgbs64}
                className="max-h-fit"
              />
            ))}
          </div>
        </section>
        {/* Card section end */}
      </main>
      <DefaultFooter />
    </>
  );
};

export default Home;

// pb-80 max-h-screen bg-red-400 flex-initial flex-col
