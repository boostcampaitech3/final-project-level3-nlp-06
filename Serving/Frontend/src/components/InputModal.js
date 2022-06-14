import React from "react";
import { useState } from "react";
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

const InputModal = (props) => {
  const [show, setShow] = useState(false);
  const [a, setA] = useState();
  const [b, setB] = useState();

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const handleSubmit = (e) => {
    //e.preventDefault();
    console.log("OPEN");
    console.log(e);
    console.log(a, b);

    setShow(false);
  };
  const handleChange1 = (e) => {
    setA(e.target.value);
  };
  const handleChange2 = (e) => {
    setB(e.target.value);
  };

  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        Launch demo modal
      </Button>

      <Modal show={show} onHide={handleClose}>
        <ModalHeader closeButton>
          <ModalTitle>Modal heading</ModalTitle>
        </ModalHeader>
        <ModalBody>
          <Form onSubmit={handleSubmit}>
            <FormGroup className="mb-3" controlId="exampleForm.ControlInput1">
              <FormLabel>Email address</FormLabel>
              <FormControl
                type="email"
                placeholder="name@example.com"
                autoFocus
                onChange={handleChange1}
              />
            </FormGroup>
            <FormGroup
              className="mb-3"
              controlId="exampleForm.ControlTextarea1"
              onChange={handleChange2}
            >
              <FormLabel>Example textarea</FormLabel>
              <FormControl as="textarea" rows={3} />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
            Save Changes
          </Button>
        </ModalFooter>
      </Modal>
    </>
  );
};

export default InputModal;
