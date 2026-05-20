import React, { useRef, useState } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';

export default function DragonMesh({ state = 'idle', health = 100 }) {
  const groupRef = useRef();
  const dragonRef = useRef();
  const [animationTime, setAnimationTime] = useState(0);
  const { canvas } = useThree();

  useFrame(() => {
    setAnimationTime(t => t + 0.016);
    const t = animationTime;

    if (!groupRef.current) return;

    switch (state) {
      case 'idle':
        if (dragonRef.current) {
          dragonRef.current.position.y = Math.sin(t * 0.4) * 0.3;
          dragonRef.current.rotation.z = Math.sin(t * 0.3) * 0.05;
          dragonRef.current.rotation.x = Math.sin(t * 0.25) * 0.03;
        }
        break;

      case 'analyzing':
        if (dragonRef.current) {
          dragonRef.current.rotation.x = Math.sin(t * 0.7) * 0.1;
          dragonRef.current.scale.y = 1 + Math.sin(t * 2) * 0.05;
        }
        break;

      case 'executing':
        if (dragonRef.current) {
          dragonRef.current.rotation.y += 0.05;
          dragonRef.current.rotation.x = Math.sin(t * 1.5) * 0.15;
          dragonRef.current.scale.set(
            1 + Math.sin(t * 3) * 0.08,
            1 + Math.cos(t * 3) * 0.08,
            1
          );
        }
        break;

      case 'warning':
        if (groupRef.current) {
          groupRef.current.rotation.z = (Math.random() - 0.5) * 0.1;
          groupRef.current.position.x = (Math.random() - 0.5) * 0.15;
        }
        break;

      case 'error':
        if (groupRef.current) {
          groupRef.current.position.y = -1;
          groupRef.current.rotation.z = Math.sin(t * 2) * 0.3;
        }
        break;

      case 'ghost':
        if (dragonRef.current) {
          dragonRef.current.position.z += 0.02;
          dragonRef.current.material.opacity = Math.max(0, 1 - t * 0.05);
        }
        break;
    }
  });

  // Crear textura del emoji dragón
  const createDragonTexture = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');

    // Fondo transparent
    ctx.clearRect(0, 0, 512, 512);

    // Dibujar emoji dragón ENORME
    ctx.font = 'bold 450px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('🐉', 256, 256);

    // Crear textura
    const texture = new THREE.CanvasTexture(canvas);
    texture.magFilter = THREE.LinearFilter;
    texture.minFilter = THREE.LinearFilter;
    return texture;
  };

  const dragonTexture = createDragonTexture();

  return (
    <group ref={groupRef} position={[0, 0, 0]}>
      {/* DRAGÓN EMOJI - PRINCIPAL */}
      <mesh ref={dragonRef} position={[0, 0, 0]} scale={[3, 3, 1]}>
        <planeGeometry args={[2, 2]} />
        <meshBasicMaterial 
          map={dragonTexture}
          transparent={true}
        />
      </mesh>

      {/* AURA ENERGÍA - detrás del dragón */}
      <mesh position={[0, 0, -0.5]}>
        <circleGeometry args={[3.5, 64]} />
        <meshBasicMaterial
          color={
            health > 75
              ? 0x00FF88
              : health > 50
              ? 0xFFFF00
              : health > 25
              ? 0xFF8800
              : 0xFF2D55
          }
          transparent={true}
          opacity={0.15}
          wireframe={true}
        />
      </mesh>

      {/* PARTÍCULAS ORBITALES */}
      {[...Array(16)].map((_, i) => {
        const angle = (i / 16) * Math.PI * 2;
        const radius = 4;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        const y = Math.sin(angle * 2.5) * 1;

        return (
          <mesh key={i} position={[x, y, z]}>
            <sphereGeometry args={[0.12, 16, 16]} />
            <meshBasicMaterial
              color={i % 2 === 0 ? 0x00FF88 : 0x00D9FF}
            />
          </mesh>
        );
      })}

      {/* ANILLO ENERGÉTICO - Rotando */}
      <mesh position={[0, 0, -0.3]} rotation={[Math.PI / 3, 0, 0]}>
        <torusGeometry args={[3, 0.2, 16, 100]} />
        <meshBasicMaterial
          color={0x00D9FF}
          transparent={true}
          opacity={0.4}
        />
      </mesh>

      {/* SEGUNDO ANILLO - Rotando en otra dirección */}
      <mesh position={[0, 0, -0.3]} rotation={[0, 0, Math.PI / 4]}>
        <torusGeometry args={[3.5, 0.15, 16, 100]} />
        <meshBasicMaterial
          color={0x00FF88}
          transparent={true}
          opacity={0.3}
        />
      </mesh>

      {/* LUCES DINÁMICAS */}
      <pointLight
        color={0x00FF88}
        intensity={3}
        distance={8}
        position={[0, 0, 1]}
      />
      <pointLight
        color={0x00D9FF}
        intensity={2}
        distance={6}
        position={[-2, 1.5, 0]}
      />
      <pointLight
        color={0xFF6600}
        intensity={1.5}
        distance={5}
        position={[2, -1.5, 0]}
      />
    </group>
  );
}
