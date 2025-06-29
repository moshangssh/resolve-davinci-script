# Active Context: Improve UI for DaVinci Smart Cut Script

**Parent Task:** Modify `davinci_smart_cut.py` to improve its user interface and interaction logic.

**Goal:** Replace static `LineEdit` inputs for track selection with dynamic `ComboBox` dropdowns, populated with actual track data from the DaVinci Resolve timeline.

---
**Log (2025-06-30 01:23):**

**1. Analysis & Planning:**
*   Reviewed `davinci_smart_cut.py` to understand the existing UI structure and data handling.
*   Analyzed `exsample.py` to learn the pattern for dynamically loading track information into UI components.
*   The key logic in `exsample.py` involves getting the timeline, querying track counts (`GetTrackCount`), and iterating to add items to a `ComboBox`.

**2. UI Implementation (`launch_ui` function):**
*   Replaced three `ui.LineEdit` controls (for source, target, and subtitle tracks) with `ui.ComboBox` controls to allow for selection instead of manual entry.
*   Added a new `ui.Button` with the label "刷新轨道" to allow users to manually refresh the track lists.
*   Grouped the "刷新轨道" and "执行" buttons together in a `ui.HGroup` for better layout.
*   Increased the window height slightly to accommodate the new layout.

**3. Track Loading Logic (`refresh_tracks` function):**
*   Created a new nested function `refresh_tracks` inside `launch_ui`.
*   This function connects to the Resolve API, gets the current timeline, and fetches all video and subtitle tracks by name.
*   Before populating, it calls `.Clear()` on each `ComboBox` to prevent duplicate entries on subsequent refreshes.
*   It populates the "源视频轨道" and "目标视频轨道" `ComboBox`es with the names of available video tracks.
*   It populates the "字幕轨道" `ComboBox` with the names of available subtitle tracks.

**4. Event Handling & Data Flow:**
*   Bound the `Clicked` event of the new "刷新轨道" button to the `refresh_tracks` function.
*   Called `refresh_tracks()` once at the end of `launch_ui` (before `dlg.Show()`) to ensure the track lists are populated when the script is first launched.
*   Modified the `run_processing` function to read the selected track names from the `ComboBox`'s `.CurrentText` property instead of the `LineEdit`'s `.Text` property.

**5. Status:**
*   All required code modifications have been applied to `davinci_smart_cut.py`. The script now features a more intuitive and error-resistant UI for track selection.