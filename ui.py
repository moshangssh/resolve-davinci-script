# -*- coding: utf-8 -*-
"""
DaVinci Resolve Smart Cut Script - UI Module
"""
import sys
from PySide2.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox
)
from PySide2.QtCore import Qt
import core

class SmartCutUI(QWidget):
    """主 UI 窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DaVinci Resolve 智能剪辑")
        self.init_ui()

    def init_ui(self):
        """初始化 UI 布局和组件"""
        layout = QVBoxLayout()

        # --- 输入字段 ---
        self.source_video_track_input = QLineEdit("Video 1")
        self.target_video_track_input = QLineEdit("Video 2")
        self.subtitle_track_input = QLineEdit("Subtitle 1")
        self.breathing_time_input = QSpinBox()
        self.breathing_time_input.setRange(0, 999)
        self.breathing_time_input.setValue(15)

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("源视频轨道:"))
        form_layout.addWidget(self.source_video_track_input)
        form_layout.addWidget(QLabel("目标视频轨道:"))
        form_layout.addWidget(self.target_video_track_input)
        form_layout.addWidget(QLabel("字幕轨道:"))
        form_layout.addWidget(self.subtitle_track_input)
        
        breathing_layout = QHBoxLayout()
        breathing_layout.addWidget(QLabel("呼吸时间 (帧):"))
        breathing_layout.addWidget(self.breathing_time_input)
        form_layout.addLayout(breathing_layout)

        layout.addLayout(form_layout)

        # --- 执行按钮 ---
        self.execute_button = QPushButton("执行")
        self.execute_button.clicked.connect(self.run_processing)
        layout.addWidget(self.execute_button)

        self.setLayout(layout)

    def run_processing(self):
        """执行核心处理逻辑"""
        source_video_track = self.source_video_track_input.text()
        target_video_track = self.target_video_track_input.text()
        subtitle_track = self.subtitle_track_input.text()
        breathing_time_frames = self.breathing_time_input.value()

        print("UI 请求执行处理...")
        
        resolve = core.get_resolve()
        if not resolve:
            print("无法连接到 Resolve。")
            return

        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        if not project:
            print("无法获取当前项目。")
            return

        timeline = project.GetCurrentTimeline()
        if not timeline:
            print("无法获取当前时间线。")
            return

        core.process_timeline(
            timeline=timeline,
            source_video_track=source_video_track,
            target_video_track=target_video_track,
            subtitle_track=subtitle_track,
            breathing_time_frames=breathing_time_frames
        )
        print("处理完成。")

def launch_ui():
    """启动 UI 应用程序"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    window = SmartCutUI()
    window.show()
    
    # 在 Resolve 的环境中，我们不希望阻塞主线程
    # 所以我们不调用 app.exec_()
    # 相反，我们让脚本执行完毕，窗口会保持打开状态

if __name__ == "__main__":
    launch_ui()