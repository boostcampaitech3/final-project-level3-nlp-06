import React, { useRef } from "react";
import { useGLTF } from "@react-three/drei";

export default function Model(props) {
  const group = useRef();
  const { nodes, materials } = useGLTF("../asset/shibe/scene.gltf");
  useGLTF.preload("..src/asset/shibe/scene.gltf");

  return (
    <group ref={group} {...props} dispose={null}>
      <mesh
        geometry={nodes.shibe.geometry}
        material={nodes.shibe.material}
        castShadow
        receiveShadow
      />
    </group>
  );
}
