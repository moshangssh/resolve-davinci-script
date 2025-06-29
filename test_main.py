# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock, patch
import sys

# 模拟 fusionscript 模块
sys.modules['fusionscript'] = MagicMock()

# 现在可以安全地导入 main 模块了
import main

class TestMain(unittest.TestCase):

    @patch('main.get_resolve')
    @patch('main.process_timeline')
    def test_main_success(self, mock_process_timeline, mock_get_resolve):
        """测试 main 函数成功执行的路径"""
        # --- Arrange ---
        # 模拟 get_resolve 返回一个有效的 Resolve 对象
        mock_resolve = MagicMock()
        mock_project_manager = MagicMock()
        mock_project = MagicMock()
        mock_timeline = MagicMock()

        mock_get_resolve.return_value = mock_resolve
        mock_resolve.GetProjectManager.return_value = mock_project_manager
        mock_project_manager.GetCurrentProject.return_value = mock_project
        mock_project.GetCurrentTimeline.return_value = mock_timeline

        # --- Act ---
        main.main()

        # --- Assert ---
        # 验证 get_resolve 被调用
        mock_get_resolve.assert_called_once()
        
        # 验证 process_timeline 被调用，并传入了正确的参数
        mock_process_timeline.assert_called_once_with(
            timeline=mock_timeline,
            source_video_track=main.SOURCE_VIDEO_TRACK,
            target_video_track=main.TARGET_VIDEO_TRACK,
            subtitle_track=main.SUBTITLE_TRACK,
            breathing_time_frames=main.BREATHING_TIME_FRAMES
        )

    @patch('main.get_resolve')
    @patch('main.process_timeline')
    def test_main_resolve_not_found(self, mock_process_timeline, mock_get_resolve):
        """测试当 get_resolve 返回 None 时的场景"""
        # --- Arrange ---
        mock_get_resolve.return_value = None

        # --- Act ---
        main.main()

        # --- Assert ---
        mock_get_resolve.assert_called_once()
        # 验证 process_timeline 未被调用
        mock_process_timeline.assert_not_called()

    @patch('main.get_resolve')
    @patch('main.process_timeline')
    def test_main_no_project_or_timeline(self, mock_process_timeline, mock_get_resolve):
        """测试当无法获取项目或时间线时的场景"""
        # --- Arrange ---
        mock_resolve = MagicMock()
        mock_project_manager = MagicMock()
        
        mock_get_resolve.return_value = mock_resolve
        mock_resolve.GetProjectManager.return_value = mock_project_manager
        # 模拟 GetCurrentProject 返回 None
        mock_project_manager.GetCurrentProject.return_value = None

        # --- Act ---
        main.main()

        # --- Assert ---
        mock_get_resolve.assert_called_once()
        mock_process_timeline.assert_not_called()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)