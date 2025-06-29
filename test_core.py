# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock, patch, call
import sys

# 模拟 fusionscript 模块，以避免在测试环境中出现 ImportError
sys.modules['fusionscript'] = MagicMock()

# 现在可以安全地导入 core 模块了
from core import process_timeline

class TestCoreProcessTimeline(unittest.TestCase):

    def setUp(self):
        """在每个测试前设置模拟对象"""
        # 创建模拟的 DaVinci Resolve 对象
        self.mock_timeline = MagicMock()
        self.mock_project = MagicMock()
        self.mock_media_pool = MagicMock()
        self.mock_media_pool_item = MagicMock()

        # 链接模拟对象
        self.mock_timeline.GetProject.return_value = self.mock_project
        self.mock_project.GetMediaPool.return_value = self.mock_media_pool

        # 默认轨道名称
        self.source_video_track = "Video 1"
        self.target_video_track = "Video 2"
        self.subtitle_track = "Subtitle 1"
        self.breathing_time = 15

    def mock_track_setup(self, video_tracks, subtitle_tracks):
        """辅助函数，用于模拟 GetTrackCount 和 GetTrackName"""
        def get_track_count(track_type):
            if track_type == "video":
                return len(video_tracks)
            if track_type == "subtitle":
                return len(subtitle_tracks)
            return 0

        def get_track_name(track_type, index):
            if track_type == "video":
                return video_tracks.get(index)
            if track_type == "subtitle":
                return subtitle_tracks.get(index)
            return None

        self.mock_timeline.GetTrackCount.side_effect = get_track_count
        self.mock_timeline.GetTrackName.side_effect = get_track_name

    def test_process_timeline_success(self):
        """测试成功处理时间线的场景"""
        # --- Arrange ---
        # 设置轨道
        self.mock_track_setup(
            video_tracks={1: self.source_video_track, 2: self.target_video_track},
            subtitle_tracks={1: self.subtitle_track}
        )

        # 创建模拟的剪辑
        mock_sub_clip = MagicMock()
        mock_sub_clip.GetStart.return_value = 1000
        mock_sub_clip.GetEnd.return_value = 1050

        mock_video_clip = MagicMock()
        mock_video_clip.GetStart.return_value = 0
        mock_video_clip.GetEnd.return_value = 5000
        mock_video_clip.GetMediaPoolItem.return_value = self.mock_media_pool_item

        self.mock_media_pool_item.GetClipProperty.return_value = "100" # Start

        self.mock_timeline.GetItemListInTrack.side_effect = [
            [mock_sub_clip],  # 字幕轨道剪辑
            [mock_video_clip]  # 源视频轨道剪辑
        ]

        # --- Act ---
        process_timeline(
            self.mock_timeline,
            self.source_video_track,
            self.target_video_track,
            self.subtitle_track,
            self.breathing_time
        )

        # --- Assert ---
        # 验证是否调用了 AppendToTimeline
        self.mock_media_pool.AppendToTimeline.assert_called_once()
        
        # 验证传递给 AppendToTimeline 的参数
        call_args = self.mock_media_pool.AppendToTimeline.call_args[0][0]
        self.assertEqual(len(call_args), 1)
        clip_info = call_args[0]
        self.assertEqual(clip_info['mediaPoolItem'], self.mock_media_pool_item)
        self.assertEqual(clip_info['startFrame'], 1100) # 100 (media start) + 1000 (offset)
        self.assertEqual(clip_info['endFrame'], 1165) # 1100 + (1050 - 1000) + 15
        self.assertEqual(clip_info['trackIndex'], 2)
        self.assertEqual(clip_info['recordFrame'], 1000)

    def test_track_not_found(self):
        """测试当一个或多个轨道未找到时的失败场景"""
        # --- Arrange ---
        # 设置不完整的轨道
        self.mock_track_setup(
            video_tracks={1: self.source_video_track}, # 目标轨道缺失
            subtitle_tracks={1: self.subtitle_track}
        )

        # --- Act ---
        process_timeline(
            self.mock_timeline,
            self.source_video_track,
            "NonExistentTrack", # 使用一个不存在的轨道名称
            self.subtitle_track,
            self.breathing_time
        )

        # --- Assert ---
        # 验证没有添加任何剪辑
        self.mock_media_pool.AppendToTimeline.assert_not_called()
        # 验证打印了错误信息 (通过检查 GetTrackName 的调用来间接验证)
        self.mock_timeline.GetTrackName.assert_any_call('video', 1)


    def test_no_subtitle_clips(self):
        """测试字幕轨道上没有剪辑的场景"""
        # --- Arrange ---
        self.mock_track_setup(
            video_tracks={1: self.source_video_track, 2: self.target_video_track},
            subtitle_tracks={1: self.subtitle_track}
        )
        # 字幕轨道返回空列表
        self.mock_timeline.GetItemListInTrack.return_value = []

        # --- Act ---
        process_timeline(
            self.mock_timeline,
            self.source_video_track,
            self.target_video_track,
            self.subtitle_track,
            self.breathing_time
        )

        # --- Assert ---
        self.mock_media_pool.AppendToTimeline.assert_not_called()

    def test_no_source_video_clip_for_subtitle(self):
        """测试字幕剪辑没有对应源视频的场景"""
        # --- Arrange ---
        self.mock_track_setup(
            video_tracks={1: self.source_video_track, 2: self.target_video_track},
            subtitle_tracks={1: self.subtitle_track}
        )

        mock_sub_clip = MagicMock()
        mock_sub_clip.GetStart.return_value = 6000
        mock_sub_clip.GetEnd.return_value = 6050

        mock_video_clip = MagicMock()
        mock_video_clip.GetStart.return_value = 0
        mock_video_clip.GetEnd.return_value = 5000 # 视频在字幕之前结束

        self.mock_timeline.GetItemListInTrack.side_effect = [
            [mock_sub_clip],
            [mock_video_clip]
        ]

        # --- Act ---
        process_timeline(
            self.mock_timeline,
            self.source_video_track,
            self.target_video_track,
            self.subtitle_track,
            self.breathing_time
        )

        # --- Assert ---
        self.mock_media_pool.AppendToTimeline.assert_not_called()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)