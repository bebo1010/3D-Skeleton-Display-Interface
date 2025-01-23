"""_summary_

Returns:
    _type_: _description_
"""

import sys
import os
import numpy as np
from vispy import scene
from canvas3d_ui import Ui_MainWindow
from vispy.scene import visuals
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from canvas3d_widget import Canvas3DView
import polars as pl


class SkeletonViewer(QMainWindow):
    """_summary_

    Args:
        QMainWindow (_type_): _description_
    """
    def __init__(self):
        super(SkeletonViewer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("3D Skeleton Viewer")
        self.resize(800, 600)

        # **用 Canvas3DView 取代 UI 內的 QWidget**
        old_widget = self.ui.canvas3d_view  # 取得 UI 內原本的 QWidget
        self.ui.canvas3d_view = Canvas3DView(parent=self.ui.centralwidget)  # 替換為 Canvas3DView

        # **用 layout 替換舊的 widget**
        layout = self.ui.verticalLayout
        layout.replaceWidget(old_widget, self.ui.canvas3d_view)
        old_widget.deleteLater()  # 刪除原本的 QWidget

        # **確保 Layout 內沒有額外邊距**
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._track_id = 1
        self.person_df = self.load_json()
        self.ui.canvas3d_view.set_datas(data=self.person_df["keypoints_3d"].to_list())
        self.timer = QTimer(self)
        self.current_frame = 1
        self.timer.timeout.connect(self.update_frame)  # 連接到更新函數
        self.timer.start(30)  # 設定每 30ms 更新一次畫面


    def load_json(self) -> pl.DataFrame:
        json_path = os.path.join( f"C0068.json")
        print(json_path)

        if not os.path.exists(json_path):
            return

        person_df = pl.read_json(json_path)
        return person_df

    def get_person_df(self, frame_num=None, is_select=False, is_kpt=False) ->pl.DataFrame:
        if self.person_df.is_empty():
            return pl.DataFrame([])

        # 條件篩選
        condition = pl.Series([True] * len(self.person_df))
        if frame_num is not None:
            condition &= self.person_df["frame_number"] == frame_num

        if is_select and self._track_id is not None:
            condition &= self.person_df["track_id"] == self._track_id

        data = self.person_df.filter(condition)
        if data.is_empty():
            return None

        if is_kpt:
            data = data["keypoints_3d"].to_list()[0]  # 獲取第一個值

        return data

    def update_frame(self):
        """更新 3D 畫面"""
        if self.person_df.is_empty():
            return

        curr_df = self.get_person_df(self.current_frame, is_select=True, is_kpt=True)
        if curr_df is not None:
            self.ui.canvas3d_view.update_points(pos=curr_df)  # 更新 3D 點位

        self.current_frame += 1
        if self.current_frame > 520:  # 假設總共有 200 幀
            self.current_frame = 1  # 重新開始動畫

# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SkeletonViewer()
    window.show()
    sys.exit(app.exec_())
