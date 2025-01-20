import sys
import numpy as np
from vispy import scene
from vispy.scene import visuals
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from src.canvas3d_widget import Canvas3DView


class SkeletonViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("3D Skeleton Viewer")
        self.resize(800, 600)

        # 创建一个 central widget
        central_widget = Canvas3DView()
        self.setCentralWidget(central_widget)

        # 创建一个布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建 VisPy 的 SceneCanvas
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', show=True)
        self.canvas.create_native()
        self.canvas.native.setParent(central_widget)

        # 将 VisPy 的 native widget 添加到布局中
        layout.addWidget(self.canvas.native)

        # 设置 3D 显示的视角
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'arcball'  # 可交互的 3D 相机
        self.view.camera.fov = 45  # 视野角度

        # 初始化骨架的3D数据 (关节坐标和连接)
        self.init_skeleton()

    def init_skeleton(self):
        # 示例：关节坐标 (假设 10 个关节)
        joints = np.array([
            [0, 0, 0],  # 身体中心
            [0, 1, 0],  # 头部
            [-0.5, 0.5, 0],  # 左肩
            [0.5, 0.5, 0],  # 右肩
            [-0.5, -0.5, 0],  # 左手
            [0.5, -0.5, 0],  # 右手
            [-0.3, -1, 0],  # 左髋
            [0.3, -1, 0],  # 右髋
            [-0.3, -1.5, 0],  # 左脚
            [0.3, -1.5, 0],  # 右脚
        ], dtype=np.float32)

        # 骨架的连接关系 (线段：起点索引, 终点索引)
        connections = np.array([
            [0, 1],  # 身体中心到头部
            [0, 2],  # 身体中心到左肩
            [0, 3],  # 身体中心到右肩
            [2, 4],  # 左肩到左手
            [3, 5],  # 右肩到右手
            [0, 6],  # 身体中心到左髋
            [0, 7],  # 身体中心到右髋
            [6, 8],  # 左髋到左脚
            [7, 9],  # 右髋到右脚
        ], dtype=np.int32)

        # 绘制关节 (点)
        joint_markers = visuals.Markers()
        joint_markers.set_data(joints, face_color='blue', size=10)
        self.view.add(joint_markers)

        # 绘制骨架 (线段)
        for connection in connections:
            start, end = joints[connection[0]], joints[connection[1]]
            line = visuals.Line(pos=np.array([start, end], dtype=np.float32), color='black', width=2)
            self.view.add(line)


# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SkeletonViewer()
    window.show()
    sys.exit(app.exec_())
