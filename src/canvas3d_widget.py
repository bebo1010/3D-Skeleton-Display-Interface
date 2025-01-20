from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from canvas3d_ui import Ui_canvas_3d_view
from datasets import coco_keypoint_info
from vispy.app import use_app
import numpy as np
import sys
from vispy import app as vis_app, visuals, scene, geometry, color
from vispy.scene.cameras import ArcballCamera, MagnifyCamera, perspective, turntable
from vispy.visuals import transforms
from vispy.color import Color

CANVAS_SIZE = (1080, 1920)  # (width, height)

class Canvas3DView(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        # self.ui = Ui_canvas_3d_view()
        # self.ui.setupUi(self)
        self.lines_plot = []
        self.canvas = scene.SceneCanvas(
            keys="interactive", show=True, size=CANVAS_SIZE, bgcolor=Color("#F2F2F2", alpha=0.2))
        self.view = self.canvas.central_widget.add_view()  # 添加视图
        # setting camera
        self.view.camera = scene.TurntableCamera(
            elevation=0, azimuth=0, roll=-90, up="+x", distance=500,translate_speed=100,
        )
        self.plane = self.set_floor_plane()
        self.set_lines_plot()


    def set_floor_plane(
        self,
        XL=12,
        YL=12,
        WS=10,
        HS=8,
        D="+z",
        translate=(3, 4, 2),
        scale=(1.0, 1.0, 1.0),
    ):
        vertices, faces, outline = geometry.create_plane(
            width=XL, height=YL, width_segments=WS, height_segments=HS, direction=D
        )
        colors = []
        for _ in range(faces.shape[0]):
            colors.append(np.array([0, 0, 0, 0.1]))
        plane = scene.visuals.Plane(
            width=XL,
            height=YL,
            width_segments=WS,
            height_segments=HS,
            direction=D,
            face_colors=np.array(colors),
            edge_color=color.color_array.Color(
                color="white", alpha=None, clip=False),
            parent=self.view.scene,
        )
        plane.transform = transforms.STTransform(
            translate=translate, scale=scale)

        return plane


    def set_lines_plot(self):
        for _ in range(len(coco_keypoint_info["keypoints"])):
            plot3D = scene.visuals.create_visual_node(visuals.LinePlotVisual)
            self.lines_plot.append(plot3D(parent=self.view.scene))

        # set traj plot
        plot3D = scene.visuals.create_visual_node(visuals.LinePlotVisual)
        self.traj_line = plot3D(parent=self.view.scene)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Canvas3DView()
    window.show()
    sys.exit(app.exec_())