import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars, Text3D, Center } from '@react-three/drei'
import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface ThreatSphereProps {
  position: [number, number, number]
  threatLevel: number
  onClick?: () => void
}

function ThreatSphere({ position, threatLevel, onClick }: ThreatSphereProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  const [hovered, setHovered] = useState(false)
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.01
      meshRef.current.rotation.y += 0.01
      const scale = hovered ? 1.2 : 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1
      meshRef.current.scale.setScalar(scale)
    }
  })
  
  const getColor = () => {
    if (threatLevel > 0.8) return '#ff003c'
    if (threatLevel > 0.5) return '#ffaa00'
    return '#00ff41'
  }
  
  return (
    <mesh
      ref={meshRef}
      position={position}
      onClick={onClick}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <icosahedronGeometry args={[0.5, 2]} />
      <meshStandardMaterial
        color={getColor()}
        emissive={getColor()}
        emissiveIntensity={0.5}
        wireframe={!hovered}
        transparent
        opacity={0.8}
      />
    </mesh>
  )
}

interface NetworkNodeProps {
  position: [number, number, number]
  isConnected: boolean
  label: string
}

function NetworkNode({ position, isConnected, label }: NetworkNodeProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  useFrame((state) => {
    if (meshRef.current && isConnected) {
      meshRef.current.material.emissiveIntensity = 0.5 + Math.sin(state.clock.elapsedTime * 3) * 0.3
    }
  })
  
  return (
    <group position={position}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshStandardMaterial
          color={isConnected ? '#00ffff' : '#666666'}
          emissive={isConnected ? '#00ffff' : '#666666'}
          emissiveIntensity={isConnected ? 0.8 : 0.2}
        />
      </mesh>
      <Text3D font="/fonts/helvetiker_regular.typeface.json" size={0.15} position={[0.5, 0, 0]}>
        {label}
        <meshStandardMaterial color="#ffffff" />
      </Text3D>
    </group>
  )
}

interface MalwareStructureProps {
  data: any[]
}

function MalwareStructure({ data }: MalwareStructureProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.005
    }
  })
  
  return (
    <group ref={groupRef}>
      {data.map((item, index) => (
        <mesh key={index} position={[Math.sin(index) * 2, Math.cos(index) * 2, index * 0.5]}>
          <boxGeometry args={[0.4, 0.4, 0.4]} />
          <meshStandardMaterial
            color="#bf00ff"
            emissive="#bf00ff"
            emissiveIntensity={0.6}
            wireframe
          />
        </mesh>
      ))}
    </group>
  )
}

interface ThreatVisualization3DProps {
  mode: 'threat' | 'network' | 'malware' | 'none'
  data?: any[]
}

export function ThreatVisualization3D({ mode, data = [] }: ThreatVisualization3DProps) {
  if (mode === 'none') return null
  
  return (
    <div className="absolute inset-0 z-0 holographic">
      <Canvas camera={{ position: [5, 5, 5], fov: 60 }}>
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
        
        {mode === 'threat' && (
          <>
            <ThreatSphere position={[0, 0, 0]} threatLevel={0.9} />
            <ThreatSphere position={[2, 1, -1]} threatLevel={0.7} />
            <ThreatSphere position={[-2, -1, 1]} threatLevel={0.4} />
            <ThreatSphere position={[1, -2, 0]} threatLevel={0.85} />
            <ThreatSphere position={[-1, 2, 1]} threatLevel={0.3} />
          </>
        )}
        
        {mode === 'network' && (
          <>
            <NetworkNode position={[0, 0, 0]} isConnected={true} label="Gateway" />
            <NetworkNode position={[3, 1, 0]} isConnected={true} label="Target-1" />
            <NetworkNode position={[-3, 2, 0]} isConnected={false} label="Target-2" />
            <NetworkNode position={[2, -2, 0]} isConnected={true} label="C2-Server" />
            
            {/* Connection lines */}
            <line>
              <bufferGeometry>
                <float32BufferAttribute attach="attributes-position" count={2} array={new Float32Array([0, 0, 0, 3, 1, 0])} itemSize={3} />
              </bufferGeometry>
              <lineBasicMaterial color="#00ffff" transparent opacity={0.5} />
            </line>
          </>
        )}
        
        {mode === 'malware' && (
          <MalwareStructure data={data.length > 0 ? data : Array(10).fill({})} />
        )}
        
        <OrbitControls enableZoom={true} enablePan={true} autoRotate autoRotateSpeed={0.5} />
      </Canvas>
    </div>
  )
}
