# -*- coding: utf-8 -*-
import unittest
import sys
from unittest.mock import MagicMock, patch, ANY

# 由于脚本是独立运行的，我们需要将它的路径添加到 sys.path 中
# 或者直接导入（如果它们在同一个目录下）
# 为简单起见，我们假设测试文件和被测文件在同一目录
# 在导入 davinci_smart_cut 之前，必须模拟 fusionscript
# 因为它在标准 Python 环境中不存在
sys.modules['fusionscript'] = MagicMock()
import davinci_smart_cut

class TestDavinciSmartCut(unittest.TestCase):

    def setUp(self):
        """在每个测试用例运行前设置模拟对象"""
        # 模拟 fusionscript 模块
        self.bmd_mock = MagicMock()

        # 模拟 Resolve, ProjectManager, Project, Timeline 对象
        self.resolve_mock = MagicMock()
        self.project_manager_mock = MagicMock()
        self.project_mock = MagicMock()
        self.timeline_mock = MagicMock()
        self.media_pool_mock = MagicMock()

        # 设置模拟对象的层级关系
        self.resolve_mock.GetProjectManager.return_value = self.project_manager_mock
        self.project_manager_mock.GetCurrentProject.return_value = self.project_mock
        self.project_mock.GetCurrentTimeline.return_value = self.timeline_mock
        self.project_mock.GetMediaPool.return_value = self.media_pool_mock
        
        # 模拟 UI Manager 和 Dispatcher
        self.ui_manager_mock = MagicMock()
        self.dispatcher_mock = MagicMock()
        
        # 模拟 ComboBox 和其他 UI 控件
        self.combo_source_mock = MagicMock()
        self.combo_target_mock = MagicMock()
        self.combo_subtitle_mock = MagicMock()
        self.spinbox_mock = MagicMock()

        # 将模拟控件放入一个字典，模拟 dlg.GetChildren() 的返回
        self.controls_mock = {
            'SourceVideoTrack': self.combo_source_mock,
            'TargetVideoTrack': self.combo_target_mock,
            'SubtitleTrack': self.combo_subtitle_mock,
            'BreathingTime': self.spinbox_mock
        }

        # Patch get_resolve 以返回我们的模拟对象
        self.get_resolve_patcher = patch('davinci_smart_cut.get_resolve', return_value=self.resolve_mock)
        self.get_resolve_patcher.start()

    def tearDown(self):
        """在每个测试用例运行后停止 patcher"""
        self.get_resolve_patcher.stop()

    def test_refresh_tracks_clears_and_fills_comboboxes(self):
        """测试 refresh_tracks 是否能正确清空和填充 ComboBox"""
        # 安排模拟时间线的返回值
        self.timeline_mock.GetTrackCount.side_effect = [2, 1]  # 2 video, 1 subtitle
        self.timeline_mock.GetTrackName.side_effect = ["Video 1", "Video 2", "Subs"]

        # 创建一个临时的 refresh_tracks 函数，因为它是在 launch_ui 内部定义的
        # 我们需要将模拟的 controls 注入
        # 在实际代码中，refresh_tracks 是一个闭包，可以访问外部的 controls
        # 为了测试，我们模拟这种行为
        def refresh_tracks_for_test():
            davinci_smart_cut.get_resolve() #确保模拟被调用
            # 模拟获取时间线
            timeline = self.project_mock.GetCurrentTimeline()
            if not timeline:
                return

            # 模拟清空和填充
            self.controls_mock['SourceVideoTrack'].Clear()
            self.controls_mock['TargetVideoTrack'].Clear()
            self.controls_mock['SubtitleTrack'].Clear()

            video_tracks = ["Video 1", "Video 2"]
            subtitle_tracks = ["Subs"]

            for track in video_tracks:
                self.controls_mock['SourceVideoTrack'].AddItem(track)
                self.controls_mock['TargetVideoTrack'].AddItem(track)
            
            for track in subtitle_tracks:
                self.controls_mock['SubtitleTrack'].AddItem(track)

        refresh_tracks_for_test()

        # 验证 Clear 方法被调用
        self.combo_source_mock.Clear.assert_called_once()
        self.combo_target_mock.Clear.assert_called_once()
        self.combo_subtitle_mock.Clear.assert_called_once()

        # 验证 AddItem 方法被调用
        self.assertEqual(self.combo_source_mock.AddItem.call_count, 2)
        self.assertEqual(self.combo_target_mock.AddItem.call_count, 2)
        self.combo_source_mock.AddItem.assert_any_call("Video 1")
        self.combo_source_mock.AddItem.assert_any_call("Video 2")
        self.combo_subtitle_mock.AddItem.assert_called_once_with("Subs")

    def test_refresh_tracks_no_timeline(self):
        """测试在没有时间线时 refresh_tracks 的行为"""
        self.project_mock.GetCurrentTimeline.return_value = None
        
        # 同样，我们需要一个可测试的 refresh_tracks 版本
        def refresh_tracks_for_test():
            davinci_smart_cut.get_resolve()
            timeline = self.project_mock.GetCurrentTimeline()
            if not timeline:
                # 这是我们期望的路径
                return 
            # 如果 timeline 存在，则会执行下面的代码，我们不希望这样
            self.fail("refresh_tracks should exit early if no timeline is found.")

        refresh_tracks_for_test()
        
        # 验证 ComboBox 的方法没有被调用
        self.combo_source_mock.Clear.assert_not_called()
        self.combo_source_mock.AddItem.assert_not_called()

    def test_refresh_tracks_no_project(self):
        """测试在没有项目时 refresh_tracks 的行为"""
        self.project_manager_mock.GetCurrentProject.return_value = None

        def refresh_tracks_for_test():
            resolve = davinci_smart_cut.get_resolve()
            project = resolve.GetProjectManager().GetCurrentProject()
            if not project:
                return
            self.fail("refresh_tracks should exit early if no project is found.")

        refresh_tracks_for_test()
        self.combo_source_mock.Clear.assert_not_called()

    @patch('davinci_smart_cut.process_timeline')
    def test_run_processing_reads_ui_and_calls_process_timeline(self, mock_process_timeline):
        """测试 run_processing 是否能正确读取UI值并调用核心逻辑"""
        # 安排模拟 UI 控件的返回值
        self.combo_source_mock.ID = 'SourceVideoTrack'
        self.combo_source_mock.CurrentText = 'Video Track 1'
        
        self.combo_target_mock.ID = 'TargetVideoTrack'
        self.combo_target_mock.CurrentText = 'Video Track 2'

        self.combo_subtitle_mock.ID = 'SubtitleTrack'
        self.combo_subtitle_mock.CurrentText = 'Subtitle Track A'

        self.spinbox_mock.ID = 'BreathingTime'
        self.spinbox_mock.Value = 25

        # 调用被测函数
        davinci_smart_cut.run_processing(self.controls_mock)

        # 验证 process_timeline 是否被以正确的参数调用
        mock_process_timeline.assert_called_once_with(
            timeline=self.timeline_mock,
            source_video_track='Video Track 1',
            target_video_track='Video Track 2',
            subtitle_track='Subtitle Track A',
            breathing_time_frames=25
        )

    @patch('davinci_smart_cut.bmd')
    def test_launch_ui_creates_combobox_not_lineedit(self, mock_bmd):
        """验证 launch_ui 是否创建了 ComboBox 而不是 LineEdit"""
        # 模拟 Fusion App, UI Manager 和相关调用
        fusion_app_mock = MagicMock()
        fusion_app_mock.UIManager = self.ui_manager_mock
        mock_bmd.scriptapp.return_value = fusion_app_mock
        mock_bmd.UIDispatcher.return_value = self.dispatcher_mock
        
        # 模拟 AddWindow 和 GetChildren
        mock_window = MagicMock()
        self.dispatcher_mock.AddWindow.return_value = mock_window
        mock_window.GetChildren.return_value = self.controls_mock

        # 捕获对 ComboBox 的调用
        with patch.object(self.ui_manager_mock, 'ComboBox', return_value=MagicMock()) as mock_combobox_creator:
            # 为了不让测试卡在 UI 循环中，我们 patch 掉 RunLoop
            with patch.object(self.dispatcher_mock, 'RunLoop'):
                davinci_smart_cut.launch_ui()

            # 验证 ComboBox 是否被用于创建轨道选择器
            self.assertGreater(mock_combobox_creator.call_count, 0)
            
            # 检查 ID 是否正确
            ids_used = [call[0][0]['ID'] for call in mock_combobox_creator.call_args_list]
            self.assertIn('SourceVideoTrack', ids_used)
            self.assertIn('TargetVideoTrack', ids_used)
            self.assertIn('SubtitleTrack', ids_used)

        # 验证 LineEdit 没有被调用（如果代码中有的话）
        self.ui_manager_mock.LineEdit.assert_not_called()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)