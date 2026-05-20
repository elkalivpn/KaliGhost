# 🐉 Dragon 3D - TECHNICAL SPECIFICATIONS & CODE TEMPLATES

**Advanced Graphics Implementation Guide**

---

## 📋 CONTENIDO

1. Dragon Mesh Technical Specs
2. Shader Implementation
3. Animation Solver Details
4. Code Scaffolding
5. Performance Optimization Tips

---

## 🐉 DRAGON MESH TECHNICAL SPECIFICATIONS

### Mesh Structure Definition

```python
"""
DRAGON MESH TOPOLOGY
=====================

Total Vertices: ~8,000 (main body) + 2,000 (detail features)
Total Faces: ~12,000 triangles
Bone Hierarchy: 48 animated joints + 150 static geometry elements

HIERARCHICAL STRUCTURE:

Root
├── Pelvis (1 joint)
│   └── Spine[0-27] (28 vertebrae, each 1 joint)
│       └── Chest
│           └── Neck[0-3] (4 neck segments)
│               └── Head (1 joint)
│                   ├── Jaw (1 joint)
│                   ├── LeftEar (1 joint)
│                   ├── RightEar (1 joint)
│                   └── Eyes[2] (2 joints, fixed pos but rotatable)
│
├── Tail[0-33] (34 tail segments, each 1 joint)
│
├── FrontLeftLeg
│   ├── Shoulder (1 joint)
│   ├── Elbow (1 joint)
│   ├── Wrist (1 joint)
│   └── Claws[0-4] (5 finger joints)
├── FrontRightLeg (symmetric)
├── BackLeftLeg (similar to front but stronger)
├── BackRightLeg (symmetric)
│
├── LeftWing
│   ├── Shoulder (1 joint)
│   ├── Elbow (1 joint)
│   ├── Wrist (1 joint)
│   ├── WingJoints[0-3] (4 finger-like structures)
│   └── Membrane (mesh, non-skeletal)
└── RightWing (symmetric)


VERTEX GROUPS & ATTRIBUTES

Each vertex stores:
├── Position (vec3): X, Y, Z coordinates
├── Normal (vec3): For lighting calculations
├── TexCoord (vec2): UV mapping for textures
├── BoneIndices (ivec4): Which 4 bones affect this vertex
├── BoneWeights (vec4): How much each bone affects (sum = 1.0)
├── Color (vec3): Base color per vertex (optional)
└── Tangent (vec3): For normal mapping

Bone Data:
├── Parent bone index
├── Local position (relative to parent)
├── Local rotation (quaternion)
├── Bounds (AABB for frustum culling)
└── Inverse bind pose matrix (for skinning)
"""

class DragonMesh:
    def __init__(self):
        self.vertices = np.zeros((8000, 3), dtype=np.float32)
        self.normals = np.zeros((8000, 3), dtype=np.float32)
        self.texcoords = np.zeros((8000, 2), dtype=np.float32)
        self.indices = np.zeros((12000 * 3,), dtype=np.uint32)
        
        # Skeletal animation data
        self.bones = {}  # bone_name -> Bone object
        self.vertex_bone_indices = np.zeros((8000, 4), dtype=np.int32)
        self.vertex_bone_weights = np.zeros((8000, 4), dtype=np.float32)
        
        # Mesh generation
        self.generate_body()
        self.generate_head()
        self.generate_wings()
        self.generate_limbs()
        self.generate_tail()
        self.compute_normals()
```

### Mesh Generation Algorithm (Body)

```python
def generate_body(self):
    """
    Generate the main body using bezier curves
    and procedural extrusion.
    """
    
    # Spine curve points (control points for bezier)
    spine_points = np.array([
        [0, 0, 0],       # Pelvis
        [0.5, 0.1, 0.2],
        [1.0, 0.15, 0.4],
        [1.5, 0.2, 0.5],
        # ... more points
        [7.0, -0.5, 0],  # End of tail region
    ])
    
    # Generate smooth curve through points
    bezier_curve = self.compute_bezier_curve(spine_points, segments=50)
    
    # At each point on curve, create a cross-section (cylinder)
    vertex_idx = 0
    for i, point in enumerate(bezier_curve):
        # Create circle of vertices (cross-section)
        radius = 0.8 * (1 - i / len(bezier_curve)) ** 0.5  # Taper
        
        for angle in np.linspace(0, 2*np.pi, 32, endpoint=False):
            x = point[0] + radius * np.cos(angle)
            y = point[1] + radius * np.sin(angle)
            z = point[2]
            
            self.vertices[vertex_idx] = [x, y, z]
            
            # Add faces connecting to previous circle
            if i > 0:
                self.connect_circles_with_faces(i-1, i, 32)
            
            vertex_idx += 1
    
    print(f"Generated {vertex_idx} vertices for body")

def compute_bezier_curve(self, points, segments=50):
    """Catmull-Rom spline interpolation"""
    curve = []
    for i in range(len(points) - 1):
        P0 = points[max(0, i-1)]
        P1 = points[i]
        P2 = points[i+1]
        P3 = points[min(len(points)-1, i+2)]
        
        for t in np.linspace(0, 1, segments):
            # Catmull-Rom basis functions
            t2 = t * t
            t3 = t2 * t
            
            q = 0.5 * (
                (2 * P1) +
                (-P0 + P2) * t +
                (2*P0 - 5*P1 + 4*P2 - P3) * t2 +
                (-P0 + 3*P1 - 3*P2 + P3) * t3
            )
            curve.append(q)
    
    return np.array(curve)
```

### Bone Configuration

```python
class Bone:
    def __init__(self, name, parent_idx, local_pos, local_rot=None):
        self.name = name
        self.parent_idx = parent_idx
        self.children_idx = []
        
        # Transform data
        self.local_position = np.array(local_pos, dtype=np.float32)
        self.local_rotation = quaternion.from_euler_angles(local_rot) if local_rot else quaternion.one
        
        # Computed transforms
        self.world_position = np.zeros(3)
        self.world_rotation = quaternion.one
        self.world_matrix = np.eye(4, dtype=np.float32)
        self.inverse_bind_pose = np.eye(4, dtype=np.float32)
        
        # Constraints
        self.rotation_limits = {
            'x': (-180, 180),  # degrees
            'y': (-180, 180),
            'z': (-180, 180)
        }
    
    def compute_world_transform(self, parent_matrix):
        """Calculate world position/rotation from parent"""
        # Local to world
        self.world_matrix = parent_matrix @ self.get_local_matrix()
        self.world_position = self.world_matrix[:3, 3]
        self.world_rotation = quaternion.from_rotation_matrix(self.world_matrix[:3, :3])

def setup_skeleton():
    """Initialize all 48 bones with proper hierarchy"""
    bones = {}
    
    # Root bone
    bones['pelvis'] = Bone('pelvis', None, [0, 0, 0])
    
    # Spine (28 bones)
    for i in range(28):
        parent = 'pelvis' if i == 0 else f'spine_{i-1}'
        z_offset = i * 0.25  # 0.25 units between each
        bones[f'spine_{i}'] = Bone(f'spine_{i}', parent, [0, 0, z_offset])
    
    # Head (connected to last spine)
    bones['neck_0'] = Bone('neck_0', 'spine_27', [0, 0.3, 0.5])
    bones['head'] = Bone('head', 'neck_0', [0.2, 0.4, 0.3])
    
    # Jaw
    bones['jaw'] = Bone('jaw', 'head', [0.1, -0.2, 0.1])
    
    # Tail (34 bones)
    for i in range(34):
        parent = 'pelvis' if i == 0 else f'tail_{i-1}'
        z_offset = -i * 0.25  # Extends backwards
        bones[f'tail_{i}'] = Bone(f'tail_{i}', parent, [0, 0, z_offset])
    
    # Limbs (8 legs)
    # Front left
    bones['front_left_shoulder'] = Bone('front_left_shoulder', 'spine_8', [-1, -1, 1])
    bones['front_left_elbow'] = Bone('front_left_elbow', 'front_left_shoulder', [-0.8, -0.8, 0])
    bones['front_left_wrist'] = Bone('front_left_wrist', 'front_left_elbow', [-0.4, -0.8, 0])
    
    # ... repeat for other limbs
    
    # Wings (8 bones per wing + membrane)
    bones['left_wing_shoulder'] = Bone('left_wing_shoulder', 'spine_12', [-0.5, 0.3, 0.2])
    bones['left_wing_elbow'] = Bone('left_wing_elbow', 'left_wing_shoulder', [-1.5, 0, 0])
    bones['left_wing_wrist'] = Bone('left_wing_wrist', 'left_wing_elbow', [-2.0, 0, 0])
    
    # ... repeat for right wing
    
    return bones
```

---

## 🎨 SHADER IMPLEMENTATION

### Vertex Shader (dragon.vert)

```glsl
#version 460 core

// Vertex attributes
layout(location = 0) in vec3 vPosition;
layout(location = 1) in vec3 vNormal;
layout(location = 2) in vec2 vTexCoord;
layout(location = 3) in ivec4 vBoneIndices;
layout(location = 4) in vec4 vBoneWeights;

// Matrices
uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;

// Skeletal animation
const int MAX_BONES = 100;
uniform mat4 uBoneMatrices[MAX_BONES];

// Output to fragment shader
out vec3 fragPosition;
out vec3 fragNormal;
out vec2 fragTexCoord;
out vec3 fragColor;

void main()
{
    // Blend bone transforms (up to 4 bones per vertex)
    mat4 blendedMatrix = 
        vBoneWeights.x * uBoneMatrices[vBoneIndices.x] +
        vBoneWeights.y * uBoneMatrices[vBoneIndices.y] +
        vBoneWeights.z * uBoneMatrices[vBoneIndices.z] +
        vBoneWeights.w * uBoneMatrices[vBoneIndices.w];
    
    // Transform position and normal
    vec4 skinnedPosition = blendedMatrix * vec4(vPosition, 1.0);
    vec3 skinnedNormal = normalize(mat3(blendedMatrix) * vNormal);
    
    // World space transformation
    fragPosition = vec3(uModel * skinnedPosition);
    fragNormal = normalize(mat3(uModel) * skinnedNormal);
    fragTexCoord = vTexCoord;
    
    // Energy coloring based on position
    float energyLevel = length(fragPosition) / 10.0;
    fragColor = vec3(0.13, 0.67, 0.33) * (0.8 + 0.2 * sin(energyLevel * 10.0));
    
    // Projected position
    gl_Position = uProjection * uView * vec4(fragPosition, 1.0);
}
```

### Fragment Shader (dragon.frag)

```glsl
#version 460 core

in vec3 fragPosition;
in vec3 fragNormal;
in vec2 fragTexCoord;
in vec3 fragColor;

uniform sampler2D uScaleTexture;
uniform sampler2D uNormalMap;
uniform vec3 uLightPos;
uniform vec3 uViewPos;
uniform float uTime;

out vec4 FragColor;

// Cyberpunk lighting with energy
vec3 computeLighting(vec3 normal, vec3 position)
{
    // Main light direction
    vec3 lightDir = normalize(uLightPos - position);
    vec3 viewDir = normalize(uViewPos - position);
    
    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = fragColor * diff * 0.8;
    
    // Specular (cyberpunk metallic look)
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = vec3(0.3, 0.7, 0.3) * spec * 0.6;
    
    // Rim light effect (cyberpunk glow)
    float rim = 1.0 - dot(viewDir, normal);
    rim = smoothstep(0.3, 1.0, rim);
    vec3 rimLight = vec3(0.0, 0.5, 1.0) * rim * 0.4;
    
    return diffuse + specular + rimLight;
}

vec3 energyPulse()
{
    // Animated energy based on time
    float pulse = sin(uTime * 2.0) * 0.5 + 0.5;
    return fragColor * pulse * 0.3;
}

void main()
{
    // Sample normal map
    vec3 normal = fragNormal;
    vec3 nmSample = texture(uNormalMap, fragTexCoord).rgb;
    normal = normalize(normal + (nmSample - 0.5) * 0.1);
    
    // Compute lighting
    vec3 lit = computeLighting(normal, fragPosition);
    
    // Add energy pulse effect
    vec3 energy = energyPulse();
    
    // Final color with bloom-ready values
    vec3 finalColor = lit + energy;
    
    // Output with alpha for transparency/energy effects
    FragColor = vec4(finalColor, 1.0);
}
```

---

## 🎬 ANIMATION SOLVER DETAILS

### Forward Kinematics Solver

```python
class ForwardKinematicsSolver:
    """
    Compute world transforms for all bones
    given their local rotations (parent → child)
    """
    
    def __init__(self, skeleton):
        self.skeleton = skeleton
        self.bone_transforms = {}
    
    def solve(self, bone_rotations_local):
        """
        bone_rotations_local: dict of bone_name -> rotation (quaternion)
        
        Returns: dict of bone_name -> world_matrix (4x4)
        """
        
        # Recursive function to traverse skeleton
        def compute_recursive(bone_name, parent_matrix):
            bone = self.skeleton[bone_name]
            
            # Apply local rotation
            if bone_name in bone_rotations_local:
                local_rot = bone_rotations_local[bone_name]
            else:
                local_rot = quaternion.one
            
            # Compute local matrix
            local_matrix = self.quaternion_to_matrix(local_rot)
            local_matrix[:3, 3] = bone.local_position
            
            # World matrix = parent * local
            world_matrix = parent_matrix @ local_matrix
            self.bone_transforms[bone_name] = world_matrix
            
            # Recursively process children
            for child_name in bone.children:
                compute_recursive(child_name, world_matrix)
        
        # Start from root
        root_matrix = np.eye(4, dtype=np.float32)
        compute_recursive('pelvis', root_matrix)
        
        return self.bone_transforms
    
    def quaternion_to_matrix(self, q):
        """Convert quaternion to 4x4 rotation matrix"""
        # Normalize quaternion
        q = q / np.linalg.norm(q)
        
        w, x, y, z = q[0], q[1], q[2], q[3]
        
        matrix = np.array([
            [1-2*y*y-2*z*z, 2*x*y-2*w*z, 2*x*z+2*w*y, 0],
            [2*x*y+2*w*z, 1-2*x*x-2*z*z, 2*y*z-2*w*x, 0],
            [2*x*z-2*w*y, 2*y*z+2*w*x, 1-2*x*x-2*y*y, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        return matrix
```

### Inverse Kinematics Solver (CCD)

```python
class IKSolverCCD:
    """
    Cyclic Coordinate Descent IK solver
    for natural limb positioning (feet on ground, etc)
    """
    
    def __init__(self, skeleton, chain_bones, iterations=10, tolerance=0.01):
        self.skeleton = skeleton
        self.chain_bones = chain_bones  # [parent, ... , end_effector]
        self.iterations = iterations
        self.tolerance = tolerance
    
    def solve(self, target_pos, fk_solver, bone_rotations):
        """
        Solve for limb positions to reach target
        
        target_pos: (x, y, z) position in world space
        fk_solver: ForwardKinematicsSolver instance
        bone_rotations: current bone rotations (will be modified)
        """
        
        end_effector_name = self.chain_bones[-1]
        
        for iteration in range(self.iterations):
            # Get current end effector position
            transforms = fk_solver.solve(bone_rotations)
            end_effector_matrix = transforms[end_effector_name]
            current_pos = end_effector_matrix[:3, 3]
            
            # Check if close enough
            error = np.linalg.norm(target_pos - current_pos)
            if error < self.tolerance:
                break
            
            # Work backwards through chain
            for i in range(len(self.chain_bones) - 2, -1, -1):
                bone_name = self.chain_bones[i]
                
                # Get world matrix of current bone
                transforms = fk_solver.solve(bone_rotations)
                bone_matrix = transforms[bone_name]
                bone_pos = bone_matrix[:3, 3]
                
                # Vector from bone to current effector
                current_vec = current_pos - bone_pos
                
                # Vector from bone to target
                target_vec = target_pos - bone_pos
                
                # Normalize
                current_vec_n = current_vec / (np.linalg.norm(current_vec) + 1e-6)
                target_vec_n = target_vec / (np.linalg.norm(target_vec) + 1e-6)
                
                # Rotation axis = cross product
                axis = np.cross(current_vec_n, target_vec_n)
                axis = axis / (np.linalg.norm(axis) + 1e-6)
                
                # Rotation angle = acos of dot product
                angle = np.arccos(np.clip(np.dot(current_vec_n, target_vec_n), -1, 1))
                
                # Apply rotation constraints
                angle = self.apply_rotation_constraints(bone_name, angle, axis)
                
                # Update bone rotation
                if angle > 1e-6:
                    axis_angle = angle * axis
                    rotation_delta = quaternion.from_rotation_vector(axis_angle)
                    bone_rotations[bone_name] = rotation_delta * bone_rotations[bone_name]
                
                # Update end effector position
                transforms = fk_solver.solve(bone_rotations)
                end_effector_matrix = transforms[end_effector_name]
                current_pos = end_effector_matrix[:3, 3]
        
        return bone_rotations
    
    def apply_rotation_constraints(self, bone_name, angle, axis):
        """Limit rotation angle to prevent unnatural poses"""
        # Most bones: limit to 45 degrees per frame
        max_angle = np.radians(45)
        
        # Special cases
        if 'spine' in bone_name:
            max_angle = np.radians(15)  # Spine less flexible
        elif 'jaw' in bone_name:
            max_angle = np.radians(30)
        
        return np.clip(angle, -max_angle, max_angle)
```

### Animation State Machine

```python
class DragonAnimationState:
    """Base class for animation states"""
    
    def __init__(self, name):
        self.name = name
        self.elapsed_time = 0.0
    
    def update(self, delta_time, fk_solver, bone_rotations):
        """Update animations for this state"""
        self.elapsed_time += delta_time
        return bone_rotations
    
    def get_priority(self):
        return 0


class RestState(DragonAnimationState):
    """Resting state: breathing and subtle movements"""
    
    def update(self, delta_time, fk_solver, bone_rotations):
        super().update(delta_time, fk_solver, bone_rotations)
        
        # Breathing animation (sine wave)
        breathing = np.sin(self.elapsed_time * 1.5) * 0.1
        
        # Apply breathing to chest bones
        for i in range(20, 25):
            bone_name = f'spine_{i}'
            # Rotate slightly around Z axis
            rot = quaternion.from_rotation_vector([0, 0, breathing])
            bone_rotations[bone_name] = rot
        
        # Tail subtle movement
        for i in range(10):
            tail_name = f'tail_{i}'
            tail_wave = np.sin(self.elapsed_time * 0.5 + i * 0.2) * 0.05
            rot = quaternion.from_rotation_vector([tail_wave, 0, 0])
            bone_rotations[tail_name] = rot
        
        return bone_rotations


class ActiveState(DragonAnimationState):
    """Active state: wing flapping, levitation"""
    
    def update(self, delta_time, fk_solver, bone_rotations):
        super().update(delta_time, fk_solver, bone_rotations)
        
        # Wing flapping (4 Hz frequency)
        wing_angle = np.sin(self.elapsed_time * 4 * 2 * np.pi) * np.pi / 4  # ±45 degrees
        
        # Left wing
        rot_left = quaternion.from_rotation_vector([wing_angle, 0, 0])
        bone_rotations['left_wing_shoulder'] = rot_left
        
        # Right wing (opposite phase)
        rot_right = quaternion.from_rotation_vector([-wing_angle, 0, 0])
        bone_rotations['right_wing_shoulder'] = rot_right
        
        # Body posture: gradually levitate
        levitation_height = min(self.elapsed_time * 0.5, 1.0)  # Over 2 seconds
        self.levitation_height = levitation_height  # Store for mesh transformation
        
        return bone_rotations


class AnimationBlender:
    """Blend between animation states"""
    
    def __init__(self, duration=0.5):
        self.blend_duration = duration
        self.blend_progress = 0.0
        self.current_state = None
        self.next_state = None
        self.blending = False
    
    def transition_to(self, new_state):
        self.next_state = new_state
        self.blending = True
        self.blend_progress = 0.0
    
    def update(self, delta_time, fk_solver, bone_rotations):
        if self.blending:
            self.blend_progress += delta_time / self.blend_duration
            
            if self.blend_progress >= 1.0:
                self.blending = False
                self.current_state = self.next_state
                self.blend_progress = 1.0
            
            # Interpolate between states
            if self.current_state and self.next_state:
                # LERP bone rotations
                blend = self.blend_progress
                
                # Get rotations from both states
                current_rots = self.current_state.update(
                    delta_time, fk_solver, bone_rotations.copy()
                )
                next_rots = self.next_state.update(
                    delta_time, fk_solver, bone_rotations.copy()
                )
                
                # Blend
                for bone_name in current_rots:
                    q1 = current_rots[bone_name]
                    q2 = next_rots[bone_name]
                    # Quaternion SLERP (spherical linear interpolation)
                    bone_rotations[bone_name] = quaternion.slerp(q1, q2, blend)
        else:
            bone_rotations = self.current_state.update(
                delta_time, fk_solver, bone_rotations
            )
        
        return bone_rotations
```

---

## 💻 CODE SCAFFOLDING TEMPLATES

### Main Application Entry Point

```python
# src/kalighost_gui/main.py

import sys
from PySide6.QtWidgets import QApplication
from kalighost_gui.app import KaliGhostProApp
from kalighost_gui.config import ConfigManager
from kalighost_gui.core.logger import setup_logging

def main():
    """Application entry point"""
    
    # Setup logging
    setup_logging()
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Load configuration
    config = ConfigManager()
    
    # Create main application
    kalighost_app = KaliGhostProApp(app, config)
    kalighost_app.show()
    
    # Run event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### Main Window Class

```python
# src/kalighost_gui/ui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QMenuBar, QToolBar, QStatusBar
)
from PySide6.QtCore import Qt

from kalighost_gui.ui.header_panel import HeaderPanel
from kalighost_gui.ui.left_sidebar import LeftSidebarPanel
from kalighost_gui.ui.viewport import MainViewport
from kalighost_gui.ui.right_sidebar import RightSidebarPanel
from kalighost_gui.ui.bottom_console import BottomConsolePanel


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("KaliGhost Pro - Professional Cyberpunk Pentesting")
        self.setGeometry(100, 100, 1920, 1080)
        
        # Setup UI
        self.setup_ui()
        self.setup_styles()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup UI layout"""
        # Central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Header
        self.header = HeaderPanel()
        main_layout.addWidget(self.header, 0)
        
        # Main content splitter
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left sidebar
        self.left_sidebar = LeftSidebarPanel()
        content_splitter.addWidget(self.left_sidebar)
        
        # Main viewport
        self.viewport = MainViewport()
        content_splitter.addWidget(self.viewport)
        
        # Right sidebar
        self.right_sidebar = RightSidebarPanel()
        content_splitter.addWidget(self.right_sidebar)
        
        # Set splitter sizes
        content_splitter.setSizes([280, 1400, 320])
        main_layout.addWidget(content_splitter, 1)
        
        # Bottom console
        self.console = BottomConsolePanel()
        main_layout.addWidget(self.console, 0)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Menubar
        self.setup_menus()
        
        # Toolbar
        self.setup_toolbar()
        
        # Statusbar
        self.statusBar().showMessage("KaliGhost Pro Ready")
    
    def setup_styles(self):
        """Apply cyberpunk theme"""
        # Import and apply theme
        from kalighost_gui.styles.themes import CyberpunkTheme
        CyberpunkTheme.apply_stylesheet(self)
    
    def setup_menus(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Project")
        file_menu.addAction("Open Project")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Help menu
        help_menu = menubar.addMenu("Help")
    
    def setup_toolbar(self):
        """Setup toolbar"""
        toolbar = self.addToolBar("Main Tools")
        toolbar.addAction("🔍 Scan")
        toolbar.addAction("⚔️ Exploit")
        toolbar.addAction("🛡️ Defense")
        toolbar.addAction("📊 Analyze")
        toolbar.addAction("📋 Report")
    
    def setup_connections(self):
        """Connect signals and slots"""
        # Connect components
        self.header.agent_status_clicked.connect(self.show_agent_details)
        self.viewport.dragon_state_changed.connect(self.right_sidebar.update_dragon_state)
        self.left_sidebar.tool_selected.connect(self.execute_tool)
    
    def show_agent_details(self):
        """Show agent details dialog"""
        # TODO: Implement
        pass
    
    def execute_tool(self, tool_name):
        """Execute selected tool"""
        # TODO: Implement
        pass
```

---

## 🚀 PERFORMANCE OPTIMIZATION TIPS

```python
"""
PERFORMANCE OPTIMIZATION CHECKLIST

Rendering:
□ Use level-of-detail (LOD) for dragon mesh
  - Far LOD: 3,000 vertices
  - Mid LOD: 8,000 vertices
  - Close LOD: 12,000 vertices

□ Batch rendering calls
  - One VBO per mesh part
  - One draw call per part (not per triangle)
  - Use instancing for particles

□ GPU memory optimization
  - Stream textures (don't load all at once)
  - Compress textures (DXT/BC formats)
  - Use indexed geometry (avoid duplicate vertices)

□ Shader optimization
  - Move complex calculations to vertex shader
  - Use precision qualifiers (lowp in mobile)
  - Avoid branching in fragment shader

Animation:
□ Skeleton caching
  - Cache bone transforms between frames if unchanged
  - Use dirty flags for unused bones

□ Animation compression
  - Use 16-bit floats for bone rotations
  - Quantize positions to 16-bit
  - Delta compression for keyframes

UI:
□ Update throttling
  - Only update right sidebar every 100ms
  - Debounce slider updates
  - Lazy load tool descriptions

□ Memory management
  - Use object pooling for temporary allocations
  - Clear caches periodically
  - Monitor for memory leaks with Valgrind

Profiling Tools:
□ nvprof (NVIDIA GPU profiler)
□ RenderDoc (graphics debugging)
□ Py-spy (Python profiler)
□ Memory_profiler (memory usage tracking)

Targets:
✓ 60 FPS sustained
✓ < 400 MB total memory
✓ < 50ms input latency
✓ < 100ms tool startup
"""
```

---

**Document Version**: 1.0  
**For**: Graphics & Animation Team

