# 系统模式

---
### 模式名称: 基于字幕的视频提取流程
[2025-06-29 16:35:21] - **描述**: 定义了脚本与 DaVinci Resolve API 交互以实现自动化剪辑的核心逻辑。

**伪代码/算法流程:**

1.  **初始化与API连接**:
    *   导入必要的库 (`fusionscript`)。
    *   获取 DaVinci Resolve 实例。
    *   获取项目管理器、当前项目和当前时间线。

2.  **读取配置**:
    *   从脚本顶部的配置区读取 `SOURCE_VIDEO_TRACK`, `TARGET_VIDEO_TRACK`, `SUBTITLE_TRACK`, `BREATHING_TIME_FRAMES`。

3.  **获取轨道对象**:
    *   通过 `timeline.GetTrackName("video", track_index)` 和 `timeline.GetTrackName("subtitle", track_index)` 验证并获取配置中指定的轨道对象。
    *   如果找不到任何一个轨道，记录错误并退出。

4.  **遍历字幕轨道**:
    *   获取字幕轨道上的所有片段列表 `subtitle_clips = timeline.GetItemListInTrack("subtitle", SUBTITLE_TRACK)`。
    *   如果列表为空，打印提示信息 "在指定字幕轨道未找到任何字幕" 并退出。

5.  **主处理循环**:
    *   对于 `subtitle_clips` 中的每一个 `clip`:
        a.  获取 `clip.Start` (起始帧)。
        b.  获取 `clip.End` (结束帧)。
        c.  计算新的结束帧: `new_end_frame = clip.End + BREATHING_TIME_FRAMES`。
        d.  在源视频轨道上查找位于 `clip.Start` 和 `new_end_frame` 时间范围内的视频片段。
        e.  **关键操作**: 使用 `timeline.Copy()` 复制找到的源视频片段。
        f.  **关键操作**: 使用 `timeline.Paste()` 将复制的片段粘贴到目标视频轨道的 `clip.Start` 位置。

6.  **完成反馈**:
    *   处理完成后，向控制台打印成功信息，例如 "处理完成！共处理 N 个字幕片段。"

**API 关键函数:**
*   `resolve.GetProjectManager().GetCurrentProject()`
*   `project.GetCurrentTimeline()`
*   `timeline.GetItemListInTrack(trackType, trackIndex)`
*   `clip.Start` / `clip.End` (属性)
*   `timeline.Copy(clip)`
*   `timeline.Paste()`