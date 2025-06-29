# -*- coding: utf-8 -*-
"""
DaVinci Resolve Smart Cut Script - All-in-One (Native UI)
Version: 2.0
Author: AI Assistant
"""
import fusionscript as bmd

# --- Core Logic ---

def get_resolve():
    """获取 DaVinci Resolve API 入口点"""
    try:
        resolve = bmd.scriptapp("Resolve")
        if resolve is None:
            print("无法连接到 DaVinci Resolve。请确保 Resolve 正在运行。")
            return None
        return resolve
    except ImportError:
        print("找不到 fusionscript 模块。请确保脚本在 DaVinci Resolve 的控制台环境中运行。")
        return None

def process_timeline(timeline, source_video_track, target_video_track, subtitle_track, breathing_time_frames):
    """
    处理时间线，根据字幕轨道提取视频片段。
    """
    project = timeline.GetProject()
    media_pool = project.GetMediaPool()

    print("核心逻辑开始执行...")
    print(f"源视频轨道: {source_video_track}")
    print(f"目标视频轨道: {target_video_track}")
    print(f"字幕轨道: {subtitle_track}")
    print(f"呼吸时间: {breathing_time_frames} 帧")

    track_indices = {"video": {}, "subtitle": {}}
    
    for track_type in ["video", "subtitle"]:
        track_count = timeline.GetTrackCount(track_type)
        for i in range(1, track_count + 1):
            track_name = timeline.GetTrackName(track_type, i)
            if track_type == "video":
                if track_name == source_video_track:
                    track_indices["video"][source_video_track] = i
                if track_name == target_video_track:
                    track_indices["video"][target_video_track] = i
            elif track_type == "subtitle":
                if track_name == subtitle_track:
                    track_indices["subtitle"][subtitle_track] = i

    source_video_track_index = track_indices["video"].get(source_video_track)
    target_video_track_index = track_indices["video"].get(target_video_track)
    subtitle_track_index = track_indices["subtitle"].get(subtitle_track)

    if not all([source_video_track_index, target_video_track_index, subtitle_track_index]):
        print("错误：一个或多个指定的轨道未在时间线上找到。")
        # ... (error reporting logic remains the same)
        return

    subtitle_clips = timeline.GetItemListInTrack("subtitle", subtitle_track_index)
    if not subtitle_clips:
        print(f"在字幕轨道 '{subtitle_track}' 上未找到任何字幕片段。")
        return

    source_clips = timeline.GetItemListInTrack("video", source_video_track_index)
    if not source_clips:
        print(f"在源视频轨道 '{source_video_track}' 上未找到任何视频片段。")
        return

    clips_to_add = []
    processed_count = 0

    for sub_clip in subtitle_clips:
        sub_start = sub_clip.GetStart()
        sub_end = sub_clip.GetEnd()
        new_end = sub_end + breathing_time_frames

        source_video_clip = None
        for vc in source_clips:
            if vc.GetStart() <= sub_start and vc.GetEnd() >= sub_end:
                source_video_clip = vc
                break
        
        if source_video_clip:
            media_pool_item = source_video_clip.GetMediaPoolItem()
            offset_in_source = sub_start - source_video_clip.GetStart()
            media_start_frame = int(media_pool_item.GetClipProperty("Start"))
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
        print(f"准备向轨道 '{target_video_track}' 添加 {len(clips_to_add)} 个剪辑...")
        media_pool.AppendToTimeline(clips_to_add)
        print(f"成功处理了 {processed_count} 个字幕片段。")
    else:
        print("没有找到可处理的字幕片段。")

    print("核心逻辑执行完毕。")

# --- UI Logic ---

def run_processing(ui_inputs):
    """执行核心处理逻辑"""
    # 初始化变量以存储从UI提取的值
    source_video_track = None
    target_video_track = None
    subtitle_track = None
    breathing_time_frames = None

    # 遍历所有UI控件以通过ID找到它们
    for control in ui_inputs.values():
        control_id = control.ID
        if control_id == 'SourceVideoTrack':
            source_video_track = control.CurrentText
        elif control_id == 'TargetVideoTrack':
            target_video_track = control.CurrentText
        elif control_id == 'SubtitleTrack':
            subtitle_track = control.CurrentText
        elif control_id == 'BreathingTime':
            breathing_time_frames = int(control.Value)

    # 验证是否所有输入都已找到
    if not all([source_video_track, target_video_track, subtitle_track, breathing_time_frames is not None]):
        print("错误：无法从UI中检索所有必需的输入。请检查UI定义。")
        return

    print("UI 请求执行处理...")
    
    resolve = get_resolve()
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

    process_timeline(
        timeline=timeline,
        source_video_track=source_video_track,
        target_video_track=target_video_track,
        subtitle_track=subtitle_track,
        breathing_time_frames=breathing_time_frames
    )
    print("处理完成。")

def launch_ui():
    """启动原生 UI"""
    try:
        fu = bmd.scriptapp('Fusion')
        ui = fu.UIManager
        disp = bmd.UIDispatcher(ui)
    except AttributeError:
        print("无法获取 Fusion/UI Manager。请在 DaVinci Resolve 的 'Fusion' 页面运行此脚本。")
        return

    # --- 创建 UI 元素 ---
    win_components = [
        ui.Label({'ID': 'Label1', 'Text': "源视频轨道:"}),
        ui.ComboBox({'ID': 'SourceVideoTrack', 'Weight': 0}),
        
        ui.Label({'ID': 'Label2', 'Text': "目标视频轨道:"}),
        ui.ComboBox({'ID': 'TargetVideoTrack', 'Weight': 0}),
        
        ui.Label({'ID': 'Label3', 'Text': "字幕轨道:"}),
        ui.ComboBox({'ID': 'SubtitleTrack', 'Weight': 0}),
        
        ui.HGroup({'Weight': 0}, [
            ui.Label({'ID': 'Label4', 'Text': "呼吸时间 (帧):"}),
            ui.SpinBox({'ID': 'BreathingTime', 'Min': 0, 'Max': 999, 'Value': 15}),
        ]),
        
        ui.HGroup({'Weight': 0}, [
            ui.Button({'ID': 'RefreshButton', 'Text': '刷新轨道'}),
            ui.Button({'ID': 'ExecuteButton', 'Text': '执行'}),
        ]),
    ]

    # --- 创建窗口定义 ---
    win = ui.VGroup(win_components)
    
    dlg = disp.AddWindow({
        'ID': 'SmartCutWin',
        'Title': 'DaVinci Resolve 智能剪辑',
        'Geometry': [600, 400, 400, 250] # X, Y, Width, Height
    }, win)

    # --- 事件处理和轨道加载 ---
    controls = dlg.GetChildren()

    def refresh_tracks():
        """获取并刷新时间线上的轨道列表"""
        print("正在刷新轨道列表...")
        resolve = get_resolve()
        if not resolve:
            return
        
        project = resolve.GetProjectManager().GetCurrentProject()
        if not project:
            return
            
        timeline = project.GetCurrentTimeline()
        if not timeline:
            print("未找到当前时间线。")
            return

        # 清空现有项目
        controls['SourceVideoTrack'].Clear()
        controls['TargetVideoTrack'].Clear()
        controls['SubtitleTrack'].Clear()

        # 加载视频轨道
        video_track_count = timeline.GetTrackCount("video")
        video_tracks = [timeline.GetTrackName("video", i) for i in range(1, video_track_count + 1)]
        for track_name in video_tracks:
            controls['SourceVideoTrack'].AddItem(track_name)
            controls['TargetVideoTrack'].AddItem(track_name)
        
        # 加载字幕轨道
        subtitle_track_count = timeline.GetTrackCount("subtitle")
        subtitle_tracks = [timeline.GetTrackName("subtitle", i) for i in range(1, subtitle_track_count + 1)]
        for track_name in subtitle_tracks:
            controls['SubtitleTrack'].AddItem(track_name)
        
        print(f"找到 {len(video_tracks)} 个视频轨道和 {len(subtitle_tracks)} 个字幕轨道。")


    def _close(ev):
        disp.ExitLoop()

    def _execute(ev):
        run_processing(controls)

    def _refresh(ev):
        refresh_tracks()

    dlg.On.SmartCutWin.Close = _close
    dlg.On.ExecuteButton.Clicked = _execute
    dlg.On.RefreshButton.Clicked = _refresh

    # 初始加载轨道
    refresh_tracks()

    print("UI 已启动。请在 UI 窗口中操作。")
    dlg.Show()
    disp.RunLoop()
    dlg.Hide()

# --- Main Execution Block ---

if __name__ == "__main__":
    print("正在启动智能剪辑 UI...")
    launch_ui()
    print("脚本执行完毕。")