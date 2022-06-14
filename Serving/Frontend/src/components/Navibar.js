import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { faBarChart } from "@fortawesome/free-regular-svg-icons";
import { faBookBookmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  Button,
  Menu,
  MenuHandler,
  MenuItem,
  MenuList,
  Navbar,
} from "@material-tailwind/react";
import React from "react";
import { Link } from "react-router-dom";
//./logo.png
const Navibar = () => {
  return (
    <Navbar className="bg-inherit text-white border-0 max-w-full h-14 mx-auto rounded-none">
      <div className="container max-w-full flex justify-between items-center ">
        <Link
          className="mx-4 flex items-center font-bold hover:text-yellow-200"
          to="/"
        >
          <img
            src="https://i.imgur.com/u27hxPa.png"
            alt="GatherBook"
            className="min-h-fit min-w-fit hover:scale-110 duration-200"
          />
        </Link>
        <div className="flex items-center lg:gap-6 gap-0">
          <Link
            className="mx-4 flex items-center font-bold hover:text-black invisible lg:visible duration-200"
            to="/about"
          >
            About Us
          </Link>
          <Link
            className="mx-4 flex items-center font-bold hover:text-black invisible lg:visible duration-200"
            to="/write"
          >
            글쓰기
          </Link>
          <Link
            className="mx-4 flex items-center font-bold hover:text-black invisible lg:visible duration-200"
            to="/tales"
          >
            구경하기
          </Link>
          <a
            className="mx-4 flex items-center font-bold hover:text-black invisible lg:visible duration-200"
            href="https://github.com/boostcampaitech3/final-project-level3-nlp-06"
          >
            <FontAwesomeIcon icon={faGithub} size="2x" />
          </a>
          <Menu className="visible lg:invisible">
            <MenuHandler>
              <Button color="amber" className="visible lg:invisible">
                <FontAwesomeIcon icon={faBarChart} size="2x" />
              </Button>
            </MenuHandler>
            <MenuList>
              <MenuItem>
                <Link
                  className="mx-4 flex items-center font-bold hover:text-amber-400"
                  to="/about"
                >
                  About Us
                </Link>
              </MenuItem>
              <MenuItem>
                <Link
                  className="mx-4 flex items-center font-bold hover:text-amber-400 "
                  to="/write"
                >
                  글쓰기
                </Link>
              </MenuItem>
              <MenuItem>
                <Link
                  className="mx-4 flex items-center font-bold hover:text-amber-400 "
                  to="/tales"
                >
                  구경하기
                </Link>
              </MenuItem>
              <MenuItem>
                <a
                  className="mx-4 flex items-center font-bold hover:text-amber-400 "
                  href="https://github.com/boostcampaitech3/final-project-level3-nlp-06"
                >
                  Github
                </a>
              </MenuItem>
            </MenuList>
          </Menu>
        </div>
      </div>
    </Navbar>
  );
};

export default Navibar;

// <FontAwesomeIcon icon={faBookBookmark} size="1x" />
// {"　GatherBook"}
