import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
} from "@material-tailwind/react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// 130자 넘으면 자르자

const TaleCard = (props) => {
  const [text, setText] = useState(props.text);
  //const defaultImg ="https://mblogthumb-phinf.pstatic.net/MjAxOTA0MTFfMyAg/MDAxNTU0OTY0NDExODM3.yq8kEVXlmOBw6q-5jyZceq2rxtUAfmCn00KjOfjf6CEg.K3qeB83x7EnikNTcr7XyDiB9Li9VOHcXV6t_6JUo7iog.PNG.goproblem/2gsjgna1uruvUuS7ndh9YqVwYGPLVszbFLwwpAYXZ1rkyz7vKAbhJvHdPRzCvhGfPWQdhkcqKLhnajnHFpGdgkDq3R1XmTFaFxUfKbVyyA3iDi1Fzv.png?type=w2";
  const defaultImg = "./duck.jpg";

  const navigate = useNavigate();
  //console.log(props);
  //console.log(props.imgbs64);

  useEffect(() => {
    console.log(props.text.length);
    if (props.text.length > 110) {
      let shot_str = props.text.substr(0, 110);
      shot_str = shot_str + "...";
      console.log(shot_str);
      setText(shot_str);
    }
  });

  const onTaleCardClick = (e) => {
    console.log(props.id);
    navigate(`/tales/${props.id}`, {
      state: {
        props,
      },
    });
  };

  // src={props.imgurl}
  // {`data:image/png;base64,${props.imgbs64}`}
  return (
    <Card
      color=""
      className="shadow-2xl border-4 border-white max-w-xs max-h-fit w-80 mt-6 hover:scale-90 transition duration-300 bg-opacity-100 scale-75x lg:scale-100 bg-myBlue"
      onClick={onTaleCardClick}
    >
      <CardHeader color="blue-grey" className="relative h-56">
        <img
          src={
            props.imgbs64
              ? `data:image/png;base64,${props.imgbs64}`
              : defaultImg
          }
          alt="img-blur-shadow"
          className="w-full h-full border-white border-4 rounded-2xl"
        />
      </CardHeader>
      <CardBody className="text-center text-white max-h-80">
        <Typography variant="h5" className="mb-2 font-woori">
          {props.title}
        </Typography>
        <Typography className="font-bold">{text}</Typography>
      </CardBody>
      <CardFooter
        divider
        className="border-white flex items-center justify-between py-3"
      >
        <Typography variant="small" color="black">
          {props.id}
        </Typography>
        <Typography variant="small" color="black" className="flex gap-1">
          <i className="fas fa-map-marker-alt fa-sm mt-[3px]" />
          {props.author}
        </Typography>
      </CardFooter>
    </Card>
  );
};

export default TaleCard;
