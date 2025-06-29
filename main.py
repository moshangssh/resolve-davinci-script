# DaVinci Resolve Smart Cut Script
# Version: 1.0
# Author: AI Assistant

import fusionscript as bmd

# --- USER CONFIGURATION ---
# 请在此处修改轨道和参数
# 源视频轨道名称 (例如: "V1")
SOURCE_VIDEO_TRACK = "Video 1"
# 目标视频轨道名称 (例如: "V2")
TARGET_VIDEO_TRACK = "Video 2"
# 字幕轨道名称 (例如: "ST1")
SUBTITLE_TRACK = "Subtitle 1"
# 在每个剪辑末尾增加的呼吸时间（以帧为单位）
BREATHING_TIME_FRAMES = 15
# --- END OF CONFIGURATION ---

def get_resolve():
    """获取 DaVinci Resolve API 入口点"""
    try:
        # 获取 Resolve Scripting API 的 fusionscript 实例
        resolve = bmd.scriptapp("Resolve")
        if resolve is None:
            print("无法连接到 DaVinci Resolve。请确保 Resolve 正在运行。")
            return None
        return resolve
    except ImportError:
        print("找不到 fusionscript 模块。请确保脚本在 DaVinci Resolve 的控制台环境中运行。")
        return None

def main():
    """主处理函数"""
    resolve = get_resolve()
    if not resolve:
        return

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    timeline = project.GetCurrentTimeline()

    if not project or not timeline:
        print("未能获取当前项目或时间线。")
        return

    print("脚本开始执行...")
    print(f"源视频轨道: {SOURCE_VIDEO_TRACK}")
    print(f"目标视频轨道: {TARGET_VIDEO_TRACK}")
    print(f"字幕轨道: {SUBTITLE_TRACK}")
    print(f"呼吸时间: {BREATHING_TIME_FRAMES} 帧")

    # --- 轨道验证与索引获取 ---
    track_indices = {
        "video": {},
        "subtitle": {}
    }
    
    for track_type in ["video", "subtitle"]:
        track_count = timeline.GetTrackCount(track_type)
        for i in range(1, track_count + 1):
            track_name = timeline.GetTrackName(track_type, i)
            if track_type == "video":
                if track_name == SOURCE_VIDEO_TRACK:
                    track_indices["video"][SOURCE_VIDEO_TRACK] = i
                if track_name == TARGET_VIDEO_TRACK:
                    track_indices["video"][TARGET_VIDEO_TRACK] = i
            elif track_type == "subtitle":
                if track_name == SUBTITLE_TRACK:
                    track_indices["subtitle"][SUBTITLE_TRACK] = i

    source_video_track_index = track_indices["video"].get(SOURCE_VIDEO_TRACK)
    target_video_track_index = track_indices["video"].get(TARGET_VIDEO_TRACK)
    subtitle_track_index = track_indices["subtitle"].get(SUBTITLE_TRACK)

    if not all([source_video_track_index, target_video_track_index, subtitle_track_index]):
        print("错误：一个或多个指定的轨道未在时间线上找到。请检查配置。")
        if not source_video_track_index:
            print(f" - 未找到源视频轨道: {SOURCE_VIDEO_TRACK}")
        if not target_video_track_index:
            print(f" - 未找到目标视频轨道: {TARGET_VIDEO_TRACK}")
        if not subtitle_track_index:
            print(f" - 未找到字幕轨道: {SUBTITLE_TRACK}")

        print("\n提示：请检查脚本顶部的配置是否与时间线上实际的轨道名称匹配。")
        print("当前时间线上的可用轨道如下：")

        # 列出所有视频轨道
        video_track_count = timeline.GetTrackCount("video")
        print("--- 视频轨道 ---")
        if video_track_count > 0:
            for i in range(1, video_track_count + 1):
                print(f"  - \"{timeline.GetTrackName('video', i)}\"")
        else:
            print("  (未找到任何视频轨道)")

        # 列出所有字幕轨道
        subtitle_track_count = timeline.GetTrackCount("subtitle")
        print("\n--- 字幕轨道 ---")
        if subtitle_track_count > 0:
            for i in range(1, subtitle_track_count + 1):
                print(f"  - \"{timeline.GetTrackName('subtitle', i)}\"")
        else:
            print("  (未找到任何字幕轨道)")

        return

    # --- 字幕遍历与视频提取 ---
    subtitle_clips = timeline.GetItemListInTrack("subtitle", subtitle_track_index)
    if not subtitle_clips:
        print(f"在字幕轨道 '{SUBTITLE_TRACK}' 上未找到任何字幕片段。")
        return

    source_clips = timeline.GetItemListInTrack("video", source_video_track_index)
    if not source_clips:
        print(f"在源视频轨道 '{SOURCE_VIDEO_TRACK}' 上未找到任何视频片段。")
        return

    media_pool = project.GetMediaPool()
    clips_to_add = []
    processed_count = 0

    for sub_clip in subtitle_clips:
        sub_start = sub_clip.GetStart()
        sub_end = sub_clip.GetEnd()
        new_end = sub_end + BREATHING_TIME_FRAMES

        # 寻找覆盖字幕片段的源视频片段
        source_video_clip = None
        for vc in source_clips:
            if vc.GetStart() <= sub_start and vc.GetEnd() >= sub_end:
                source_video_clip = vc
                break
        
        if source_video_clip:
            media_pool_item = source_video_clip.GetMediaPoolItem()
            
            # 计算在源媒体文件中的偏移量
            offset_in_source = sub_start - source_video_clip.GetStart()
            
            # 获取源媒体的起始帧
            media_start_frame = int(media_pool_item.GetClipProperty("Start"))

            # 计算新剪辑在源媒体中的入点和出点
            new_clip_start_in_media = media_start_frame + offset_in_source
            new_clip_end_in_media = new_clip_start_in_media + (new_end - sub_start)

            clip_info = {
                "mediaPoolItem": media_pool_item,
                "startFrame": new_clip_start_in_media,
                "endFrame": new_clip_end_in_media,
                "trackIndex": target_video_track_index,
                "recordFrame": sub_start
            }
            clips_to_add.append(clip_info)
            processed_count += 1
        else:
            print(f"警告：在时间 {sub_start} 未找到对应的源视频片段，跳过此字幕。")

    if clips_to_add:
        print(f"准备向轨道 '{TARGET_VIDEO_TRACK}' 添加 {len(clips_to_add)} 个剪辑...")
        media_pool.AppendToTimeline(clips_to_add)
        print(f"成功处理了 {processed_count} 个字幕片段。")
    else:
        print("没有找到可处理的字幕片段。")

    print("脚本执行完毕。")

if __name__ == "__main__":
    main()