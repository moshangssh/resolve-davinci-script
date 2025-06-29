import unittest
from unittest.mock import MagicMock, patch, call
import io
import sys

# 由于 main.py 可能会导入 fusionscript，我们必须在测试开始前模拟它
# 否则，在没有 DaVinci Resolve 环境的情况下，`import main` 会直接失败
sys.modules['fusionscript'] = MagicMock()

import main

class TestResolveScript(unittest.TestCase):

    def setUp(self):
        """在每个测试用例开始前，重置模拟对象和标准输出捕获"""
        # 模拟 DaVinci Resolve 的 API 对象结构
        self.mock_bmd = sys.modules['fusionscript']
        self.mock_resolve = MagicMock()
        self.mock_project_manager = MagicMock()
        self.mock_project = MagicMock()
        self.mock_timeline = MagicMock()
        self.mock_media_pool = MagicMock()

        # 设置模拟对象的返回关系
        self.mock_bmd.scriptapp.return_value = self.mock_resolve
        self.mock_resolve.GetProjectManager.return_value = self.mock_project_manager
        self.mock_project_manager.GetCurrentProject.return_value = self.mock_project
        self.mock_project.GetCurrentTimeline.return_value = self.mock_timeline
        self.mock_project.GetMediaPool.return_value = self.mock_media_pool

        # 捕获 print() 函数的输出
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        """在每个测试用例结束后，恢复标准输出"""
        sys.stdout = self.held_stdout

    def test_get_resolve_success(self):
        """测试 get_resolve 成功连接的情况"""
        with patch('main.bmd', self.mock_bmd):
            resolve_instance = main.get_resolve()
            self.assertIsNotNone(resolve_instance)
            self.mock_bmd.scriptapp.assert_called_with("Resolve")

    def test_get_resolve_connection_failed(self):
        """测试 get_resolve 无法连接到 Resolve 的情况"""
        self.mock_bmd.scriptapp.return_value = None
        with patch('main.bmd', self.mock_bmd):
            resolve_instance = main.get_resolve()
            self.assertIsNone(resolve_instance)
            output = sys.stdout.getvalue()
            self.assertIn("无法连接到 DaVinci Resolve", output)

    def test_main_no_project_or_timeline(self):
        """测试当没有活动项目或时间线时的错误处理"""
        self.mock_project.GetCurrentTimeline.return_value = None
        with patch('main.get_resolve', return_value=self.mock_resolve):
            main.main()
            output = sys.stdout.getvalue()
            self.assertIn("未能获取当前项目或时间线", output)

    def test_track_lookup_success(self):
        """测试所有轨道都能被成功找到的情况"""
        # --- 更详细的模拟设置 ---
        # 1. 模拟轨道名称查找
        def mock_get_track_name(track_type, index):
            if track_type == "video":
                return {1: main.SOURCE_VIDEO_TRACK, 2: main.TARGET_VIDEO_TRACK}.get(index)
            if track_type == "subtitle":
                return {1: main.SUBTITLE_TRACK}.get(index)
            return None
        
        self.mock_timeline.GetTrackCount.side_effect = lambda t: 2 if t == "video" else 1
        self.mock_timeline.GetTrackName.side_effect = mock_get_track_name

        # 2. 模拟剪辑及其属性
        mock_sub_clip = MagicMock()
        mock_sub_clip.GetStart.return_value = 100
        mock_sub_clip.GetEnd.return_value = 200

        mock_video_clip = MagicMock()
        mock_video_clip.GetStart.return_value = 0
        mock_video_clip.GetEnd.return_value = 1000
        mock_media_pool_item = MagicMock()
        mock_media_pool_item.GetClipProperty.return_value = "0" # Start frame
        mock_video_clip.GetMediaPoolItem.return_value = mock_media_pool_item

        # 3. 模拟轨道上的剪辑列表
        def mock_get_item_list(track_type, index):
            if track_type == "subtitle":
                return [mock_sub_clip]
            if track_type == "video":
                return [mock_video_clip]
            return []
        
        self.mock_timeline.GetItemListInTrack.side_effect = mock_get_item_list
        self.mock_media_pool.AppendToTimeline.return_value = True

        with patch('main.get_resolve', return_value=self.mock_resolve):
            main.main()
            output = sys.stdout.getvalue()
            
            # 关键断言：不应出现轨道未找到的错误
            self.assertNotIn("错误：一个或多个指定的轨道未在时间线上找到", output)
            self.assertIn(f"准备向轨道 '{main.TARGET_VIDEO_TRACK}' 添加 1 个剪辑...", output)
            self.mock_media_pool.AppendToTimeline.assert_called_once()

    def test_track_lookup_fails_source_video_track_missing(self):
        """测试当源视频轨道未找到时的错误处理"""
        # 模拟轨道名称查找函数
        def mock_get_track_name(track_type, index):
            if track_type == "video":
                return {1: "Some Other Track", 2: main.TARGET_VIDEO_TRACK}.get(index)
            if track_type == "subtitle":
                return {1: main.SUBTITLE_TRACK}.get(index)
            return None

        self.mock_timeline.GetTrackCount.side_effect = lambda t: 2 if t == "video" else 1
        self.mock_timeline.GetTrackName.side_effect = mock_get_track_name

        with patch('main.get_resolve', return_value=self.mock_resolve):
            main.main()
            output = sys.stdout.getvalue()
            # 检查是否打印了主错误信息
            self.assertIn("错误：一个或多个指定的轨道未在时间线上找到", output)
            # 检查是否明确指出了哪个轨道未找到
            self.assertIn(f"- 未找到源视频轨道: {main.SOURCE_VIDEO_TRACK}", output)
            # 检查是否列出了可用的轨道以供用户参考
            self.assertIn('--- 视频轨道 ---', output)
            self.assertIn('- "Some Other Track"', output)
            self.assertIn(f'- "{main.TARGET_VIDEO_TRACK}"', output)

    def test_track_lookup_fails_all_tracks_missing(self):
        """测试所有指定轨道都未找到时的错误处理"""
        # 模拟轨道名称查找函数
        def mock_get_track_name(track_type, index):
            if track_type == "video":
                return {1: "Track A", 2: "Track B"}.get(index)
            if track_type == "subtitle":
                return {1: "Track C"}.get(index)
            return None

        self.mock_timeline.GetTrackCount.side_effect = lambda t: 2 if t == "video" else 1
        self.mock_timeline.GetTrackName.side_effect = mock_get_track_name

        with patch('main.get_resolve', return_value=self.mock_resolve):
            main.main()
            output = sys.stdout.getvalue()
            self.assertIn("错误：一个或多个指定的轨道未在时间线上找到", output)
            self.assertIn(f"- 未找到源视频轨道: {main.SOURCE_VIDEO_TRACK}", output)
            self.assertIn(f"- 未找到目标视频轨道: {main.TARGET_VIDEO_TRACK}", output)
            self.assertIn(f"- 未找到字幕轨道: {main.SUBTITLE_TRACK}", output)
            self.assertIn('- "Track A"', output)
            self.assertIn('- "Track B"', output)
            self.assertIn('- "Track C"', output)

    def test_no_subtitle_clips_found(self):
        """测试当字幕轨道上没有剪辑时的错误处理"""
        # 轨道查找成功
        self.mock_timeline.GetTrackCount.side_effect = lambda type: 2 if type == "video" else 1
        self.mock_timeline.GetTrackName.side_effect = [
            main.SOURCE_VIDEO_TRACK, main.TARGET_VIDEO_TRACK,
            main.SUBTITLE_TRACK
        ]
        # 关键模拟：字幕轨道返回空列表
        self.mock_timeline.GetItemListInTrack.side_effect = lambda type, index: [] if type == "subtitle" else [MagicMock()]

        with patch('main.get_resolve', return_value=self.mock_resolve):
            main.main()
            output = sys.stdout.getvalue()
            self.assertIn(f"在字幕轨道 '{main.SUBTITLE_TRACK}' 上未找到任何字幕片段。", output)
            # 确认没有进入剪辑处理阶段
            self.assertNotIn("准备向轨道", output)

    def test_no_source_video_clips_found(self):
        """测试当源视频轨道上没有剪辑时的错误处理"""
        # 轨道查找成功
        self.mock_timeline.GetTrackCount.side_effect = lambda type: 2 if type == "video" else 1
        self.mock_timeline.GetTrackName.side_effect = [
            main.SOURCE_VIDEO_TRACK, main.TARGET_VIDEO_TRACK,
            main.SUBTITLE_TRACK
        ]
        # 关键模拟：视频轨道返回空列表
        self.mock_timeline.GetItemListInTrack.side_effect = lambda type, index: [MagicMock()] if type == "subtitle" else []

        with patch('main.get_resolve', return_value=self.mock_resolve):
            main.main()
            output = sys.stdout.getvalue()
            self.assertIn(f"在源视频轨道 '{main.SOURCE_VIDEO_TRACK}' 上未找到任何视频片段。", output)
            self.assertNotIn("准备向轨道", output)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)