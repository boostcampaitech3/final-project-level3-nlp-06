import { Button, IconButton, Textarea } from "@material-tailwind/react";
import axios from "axios";
import React, { useEffect, useState } from "react";
import Navibar from "../components/Navibar";
import TaleCard from "../components/Talecard";
import { SERVER_ADDRESS } from "../constants";

const Test = () => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const onClick = (e) => {
    setModalIsOpen(true);
  };

  return (
    <>
      <div className=""></div>
      <main>
        <Button onClick={onClick}>button</Button>
      </main>
    </>
  );
};

export default Test;

//TODO: [중요] 시연 영상 녹화 -> 목요일 오전까지
