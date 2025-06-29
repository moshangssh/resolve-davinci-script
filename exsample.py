# pip install googletrans==4.0.0-rc1
 
 
# import DaVinciResolveScript as bmd
import os
import math
import time
import random
 
def getresolve(app='Resolve'):
    return bmd.scriptapp(app)
 
def get_fusion():
    return getresolve('Fusion')
 
def this_pj():
    resolve = getresolve()
    pj_manager = resolve.GetProjectManager()
    current_pj = pj_manager.GetCurrentProject()
    return current_pj
 
def this_timeline():
    timeline = this_pj().GetCurrentTimeline()
    return timeline
def aDD_timeline():
    media_pool = this_pj().GetMediaPool()
    tt = this_timeline()
    v_index = track   #视频轨道
    #导入文件夹
    folder_path =r'C:\Users'
    s_index = track02 #字幕轨道
    # print(s_index)
    file_list = os.listdir(folder_path)
    dq_file = media_pool.GetCurrentFolder().GetName()
    current_folderks = media_pool.GetCurrentFolder()
 
 
    def del_clip():   #删除时间线
        dhfj = current_folderks.GetSubFolderList()
        for index, value in enumerate(dhfj):
            if value.GetName() == '__RS_TextPlus_FPS__':
               media_pool.DeleteFolders([dhfj[index]])
 
 
 
    # 导入文件夹中的素材到DaVinci Resolve项目
    for file_name in file_list:
        if file_name == '__RS_TextPlus_FPS__.drb':
        # 构建完整的文件路径
            file_path = os.path.join(folder_path, file_name)
            # print(file_path)
 
            # 导入素材
            # media_pool = project.GetMediaPool()
            media_pool.ImportFolderFromFile(file_path)    #导入指定文件
        folder_name = "__RS_TextPlus_FPS__"
 
        # 获取媒体池中的文件夹列表
        folder_list = media_pool.GetCurrentFolder().GetSubFolderList()
        # print(folder_list)
 
        # 在文件夹列表中查找指定名称的文件夹
        target_folder = None
        for folder in folder_list:
 
            B = folder.GetName()
            # print(B)
            if B == folder_name:
                target_folder = folder
                break
 
        # 如果找到了目标文件夹，则打开它
        if target_folder:
            media_pool.SetCurrentFolder(target_folder)
            # print("Opened folder:", folder_name)
        else:
            print(f"代号001")
 
    # print("导入完毕！")
 
    fps = tt.GetSetting("timelineFrameRate")
    text_template = None
 
    current_folder = media_pool.GetCurrentFolder()
    # print(current_folder)
 
 
    for clip in current_folder.GetClipList():
        name = clip.GetClipProperty('Clip Name')
        name2 = f'TextPlus{fps}FPS'
        if str(name[0:10]) == str(name2[0:10]):
            text_template = clip
            # print(clip)
            break
 
 
    for item in tt.GetItemListInTrack('subtitle', s_index):  #添加到时间线
        sf = item.GetStart()
        ef = item.GetEnd()
        text = item.GetName()
        text_plus = media_pool.AppendToTimeline([{
            'mediaPoolItem': text_template,
            'startFrame': 0,
            'endFrame': ef - sf - 1,
            'trackIndex': v_index,
            'mediaType': 1,
            'recordFrame': sf,
        }])[0]
        # print(text_plus)
        # for sc in tt.GetItemListInTrack("video",v_index):
        #     n = sc.GetName()
        comp = text_plus.GetFusionCompByIndex(1)
        lst = comp.GetToolList(False, 'TextPlus')
        tool = lst[1]
 
        comp.StartUndo('RS Jimaku')  # 开始撤销操作
        comp.Lock()  # 锁定合成
        try:
            path2 = str(selected02)
            st = bmd.readfile(path2)
            if st is not None:
                if len(itm['r_path0002'].Text) > 1:
                    tool.LoadSettings(st)
                else:
                    tool.Font = 'Microsoft YaHei UI'  # 设置字体
 
        except NameError as e:
            print("没检测到模板文件，将按照常规添加字幕！")
            tool.Font = 'Microsoft YaHei UI'  # 设置字体
        pass
 
        # tool.StyledText = text
 
        tool.StyledText = text  # 设置文本内容
        tool.UseFrameFormatSettings = 1  # 使用框架格式设置
        comp.Unlock()
        comp.EndUndo(True)
    del_clip()
 
 
 
def aDD_timelineZH():
    # from googletrans import Translator
    # translator = Translator()
    from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
    import warnings
    # 忽略警告信息
    warnings.filterwarnings('ignore')
    modelName = "Helsinki-NLP/opus-mt-en-zh"
    itm['r_path022'].Text = "正在加载翻译模型...."
    model = AutoModelForSeq2SeqLM.from_pretrained(modelName)
    # 使用 AutoTokenizer 加载对应的分词器
    tokenizer = AutoTokenizer.from_pretrained(modelName)
 
    # 创建翻译管道，这里翻译从中文到英文
    translation = pipeline('translation', model=model, tokenizer=tokenizer)
 
    # 设置要加载的翻译模型名称，Helsinki-NLP/opus-mt-zh-en 是一个中文到英文的翻译模型
    modelName = "Helsinki-NLP/opus-mt-zh-en"
    media_pool = this_pj().GetMediaPool()
    tt = this_timeline()
    v_index = track   #视频轨道
    #导入文件夹
    folder_path =r'C:\Users'
    s_index = track02 #字幕轨道
    print(s_index)
    file_list = os.listdir(folder_path)
    dq_file = media_pool.GetCurrentFolder().GetName()
    current_folderks = media_pool.GetCurrentFolder()
 
 
    def del_clip():   #删除时间线
        dhfj = current_folderks.GetSubFolderList()
        for index, value in enumerate(dhfj):
            if value.GetName() == '__RS_TextPlus_FPS__':
               media_pool.DeleteFolders([dhfj[index]])
 
 
 
    # 导入文件夹中的素材到DaVinci Resolve项目
    for file_name in file_list:
        if file_name == '__RS_TextPlus_FPS__.drb':
        # 构建完整的文件路径
            file_path = os.path.join(folder_path, file_name)
            # print(file_path)
 
            # 导入素材
            # media_pool = project.GetMediaPool()
            media_pool.ImportFolderFromFile(file_path)    #导入指定文件
        folder_name = "__RS_TextPlus_FPS__"
 
        # 获取媒体池中的文件夹列表
        folder_list = media_pool.GetCurrentFolder().GetSubFolderList()
        # print(folder_list)
 
        # 在文件夹列表中查找指定名称的文件夹
        target_folder = None
        for folder in folder_list:
 
            B = folder.GetName()
            # print(B)
            if B == folder_name:
                target_folder = folder
                break
 
        # 如果找到了目标文件夹，则打开它
        if target_folder:
            media_pool.SetCurrentFolder(target_folder)
            print("Opened folder:", folder_name)
        else:
            print("Folder not found:", folder_name)
 
    print("导入完毕！")
 
    fps = tt.GetSetting("timelineFrameRate")
    text_template = None
 
    current_folder = media_pool.GetCurrentFolder()
    print(current_folder)
 
 
    for clip in current_folder.GetClipList():
        name = clip.GetClipProperty('Clip Name')
 
        name2 = f'TextPlus{fps}FPS'
        if str(name[0:10]) == str(name2[0:10]):
            text_template = clip
            # print(clip)
            break
 
 
    for item in tt.GetItemListInTrack('subtitle', s_index):  #添加到时间线
        sf = item.GetStart()
        ef = item.GetEnd()
        text = item.GetName()
        text_plus = media_pool.AppendToTimeline([{
            'mediaPoolItem': text_template,
            'startFrame': 0,
            'endFrame': ef - sf - 1,
            'trackIndex': v_index,
            'mediaType': 1,
            'recordFrame': sf,
        }])[0]
        # print(text_plus)
        # for sc in tt.GetItemListInTrack("video",v_index):
        #     n = sc.GetName()
        comp = text_plus.GetFusionCompByIndex(1)
        lst = comp.GetToolList(False, 'TextPlus')
        tool = lst[1]
 
        comp.StartUndo('RS Jimaku')  # 开始撤销操作
        comp.Lock()  # 锁定合成
        try:
            path2 = str(selected02)
            st = bmd.readfile(path2)
            if st is not None:
                if len(itm['r_path0002'].Text) > 1:
                    tool.LoadSettings(st)
                else:
                    tool.Font = 'Microsoft YaHei UI'  # 设置字体
        except NameError as e:
            print("没检测到模板文件，将按照常规添加字幕！")
            tool.Font = 'Microsoft YaHei UI'  # 设置字体
        pass
 
        res = translation(text)[0]['translation_text']
        tool.StyledText = res  # 设置文本内容
        tool.UseFrameFormatSettings = 1  # 使用框架格式设置
        comp.Unlock()  # 解锁合成
        comp.EndUndo(True)  # 结束撤销操作
        itm['r_path022'].Text = f"{text} 》》正在翻译...."
        # time.sleep(random.uniform(5, 15))
    del_clip()
 
 
def aDD_timelineEN():
    from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
    import warnings
    # 忽略警告信息
    warnings.filterwarnings('ignore')
    modelName = "Helsinki-NLP/opus-mt-zh-en"
    itm['r_path022'].Text = "正在加载翻译模型...."
    model = AutoModelForSeq2SeqLM.from_pretrained(modelName)
    # 使用 AutoTokenizer 加载对应的分词器
    tokenizer = AutoTokenizer.from_pretrained(modelName)
 
    # 创建翻译管道，这里翻译从中文到英文
    translation = pipeline('translation', model=model, tokenizer=tokenizer)
 
    # 设置要加载的翻译模型名称，Helsinki-NLP/opus-mt-zh-en 是一个中文到英文的翻译模型
    modelName = "Helsinki-NLP/opus-mt-zh-en"
    media_pool = this_pj().GetMediaPool()
    tt = this_timeline()
    v_index = track   #视频轨道
    #导入文件夹
    folder_path =r'C:\Users'
    s_index = track02 #字幕轨道
    print(s_index)
    file_list = os.listdir(folder_path)
    dq_file = media_pool.GetCurrentFolder().GetName()
    current_folderks = media_pool.GetCurrentFolder()
 
 
    def del_clip():   #删除时间线
        dhfj = current_folderks.GetSubFolderList()
        for index, value in enumerate(dhfj):
            if value.GetName() == '__RS_TextPlus_FPS__':
               media_pool.DeleteFolders([dhfj[index]])
 
 
 
    # 导入文件夹中的素材到DaVinci Resolve项目
    for file_name in file_list:
        if file_name == '__RS_TextPlus_FPS__.drb':
        # 构建完整的文件路径
            file_path = os.path.join(folder_path, file_name)
            # print(file_path)
 
            # 导入素材
            # media_pool = project.GetMediaPool()
            media_pool.ImportFolderFromFile(file_path)    #导入指定文件
        folder_name = "__RS_TextPlus_FPS__"
 
        # 获取媒体池中的文件夹列表
        folder_list = media_pool.GetCurrentFolder().GetSubFolderList()
        # print(folder_list)
 
        # 在文件夹列表中查找指定名称的文件夹
        target_folder = None
        for folder in folder_list:
 
            B = folder.GetName()
            # print(B)
            if B == folder_name:
                target_folder = folder
                break
 
        # 如果找到了目标文件夹，则打开它
        if target_folder:
            media_pool.SetCurrentFolder(target_folder)
            print("Opened folder:", folder_name)
        else:
            print("Folder not found:", folder_name)
 
    print("导入完毕！")
 
    fps = tt.GetSetting("timelineFrameRate")
    text_template = None
 
    current_folder = media_pool.GetCurrentFolder()
    print(current_folder)
 
 
    for clip in current_folder.GetClipList():
        name = clip.GetClipProperty('Clip Name')
 
        name2 = f'TextPlus{fps}FPS'
        if str(name[0:10]) == str(name2[0:10]):
            text_template = clip
            # print(clip)
            break
 
 
    for item in tt.GetItemListInTrack('subtitle', s_index):  #添加到时间线
        sf = item.GetStart()
        ef = item.GetEnd()
        text = item.GetName()
        text_plus = media_pool.AppendToTimeline([{
            'mediaPoolItem': text_template,
            'startFrame': 0,
            'endFrame': ef - sf - 1,
            'trackIndex': v_index,
            'mediaType': 1,
            'recordFrame': sf,
        }])[0]
        # print(text_plus)
        # for sc in tt.GetItemListInTrack("video",v_index):
        #     n = sc.GetName()
        comp = text_plus.GetFusionCompByIndex(1)
        lst = comp.GetToolList(False, 'TextPlus')
        tool = lst[1]
 
        comp.StartUndo('RS Jimaku')  # 开始撤销操作
        comp.Lock()  # 锁定合成
        try:
            path2 = str(selected02)
            st = bmd.readfile(path2)
            if st is not None:
                if len(itm['r_path0002'].Text) > 1:
                    tool.LoadSettings(st)
                else:
                    tool.Font = 'Microsoft YaHei UI'  # 设置字体
        except NameError as e:
            print("没检测到模板文件，将按照常规添加字幕！")
            tool.Font = 'Microsoft YaHei UI'  # 设置字体
        pass
 
        # tool.Font = 'PingFang SC'  # 设置字体
 
        res = translation(text)[0]['translation_text']
        tool.StyledText = res  # 设置文本内容
        tool.UseFrameFormatSettings = 1  # 使用框架格式设置
        comp.Unlock()  # 解锁合成
        comp.EndUndo(True)  # 结束撤销操作
        itm['r_path022'].Text = f"{text} 》》正在翻译...."
        # time.sleep(random.uniform(5, 15))
    del_clip()
        # print("字幕添加完成")
def ouputSRT():
    def to_time(fps, frame) -> str:
        float_sec = int(frame) / int(fps)
        sec = math.floor(float_sec)
        ms = round((float_sec - sec) * 1000)
        minute, sec = divmod(sec, 60)
        hour, minute = divmod(minute, 60)
        return '%02d:%02d:%02d,%03d' % (hour, minute, sec, ms)
 
    srt_file = path
    index = track
    timeline = this_timeline()
    timeline_name = timeline.GetName()
 
    start_frame = timeline.GetStartFrame()
    fps = timeline.GetSetting("timelineFrameRate")
    data_list = []
    for i, item in enumerate(timeline.GetItemListInTrack('video', index)):
        if item.GetFusionCompCount() == 0:
            continue
        comp = item.GetFusionCompByIndex(1)
        lst = comp.GetToolList(False, 'TextPlus')  # 获取TextPlus工具列表
        if not lst[1]:
            continue
        s_text = to_time(fps, item.GetStart() - start_frame)  # 获取开始时间
        e_text = to_time(fps, item.GetEnd() - start_frame)  # 获取结束时间
        text = lst[1].GetInput('StyledText', 0)  # 获取TextPlus中的文本内容
 
        # 将字幕数据格式化为 SRT 格式
        lst = [
            str(i + 1),
            s_text + ' --> ' + e_text,
            text,
        ]
        data_list.append('\n'.join(lst))  # 添加到数据列表中
    file_name = f"{timeline_name} 字幕文件.srt"
    file_path = os.path.join(srt_file, file_name)
    # print(file_path)
    srt = '\n\n'.join(data_list)  # 合并所有字幕数据
    # print(srt)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(srt)
    # print("字幕导出完毕")
 
 
def tihuanzimu(ev):
    track = int(itm['tracknum'].CurrentText)  # 获取当前选择的视频轨道数
    yuanlai01 = itm['yuanlai'].GetText()
    tihuan02 = itm['tihuan'].GetText()
    yuanlai =str(yuanlai01)
    tihuan = str(tihuan02)
    if len(yuanlai) < 1:
        print("请输入要替换的文字")
        itm['r_path022'].Text = "请输入要替换的文字！！！"
    else:
        # 替换的目标词语及其替代词
        replacements = {
            yuanlai: tihuan,
        }
        timeline = this_timeline()
        track_clips = timeline.GetItemsInTrack("video",track)
        if len(track_clips) < 1:
            print("请正确选择轨道")
            itm['r_path022'].Text = "请正确选择轨道！"
 
 
        # print(track_clips)
        # 直接使用for循环进行替换
        try:
            for clip_id, clip in track_clips.items():
                comp = clip.GetFusionCompByIndex(1)
                lst = comp.GetToolList(False, 'TextPlus')
                tool = lst[1]
                toolname = tool.GetInput("StyledText")
                if yuanlai in toolname:
                    new_sentence = toolname.replace(yuanlai, tihuan)
                    comp = clip.GetFusionCompByIndex(1)
                    lst = comp.GetToolList(False, 'TextPlus')
                    tool = lst[1]
                    tool.StyledText = new_sentence  # 设置文本内容
                    print(f"{new_sentence}_替换成功")
                    itm['r_path022'].Text = f"{new_sentence}替换成功"
                    itm['r_path022'].Text = "全部文字替换完毕"
                else:
                    print(f"{toolname}目标词语未找到，跳过替换。")
        except Exception as e:
           print("请选择Text+的文字轨道")
           itm['r_path022'].Text = "请选择Text+的文字轨道!"
 
 
 
 
 
 
def load_track_count():  # 定义加载视频轨道数量的函数
    itm['tracknum'].Clear()  # 清空视频轨道下拉框中的所有选项
    v_track = int(this_timeline().GetTrackCount('video'))  # 获取视频轨道的数量
    for i in range(1, v_track + 1):  # 遍历所有视频轨道
        itm['tracknum'].AddItem(str(i))  # 将轨道数量添加到轨道数下拉框中
 
 
def load_track_count02():  # 定义加载视频轨道数量的函数
    itm['tracknum02'].Clear()  # 清空视频轨道下拉框中的所有选项
    v_track = int(this_timeline().GetTrackCount('subtitle'))  # 获取视频轨道的数量
    for i in range(1, v_track + 1):  # 遍历所有视频轨道
        itm['tracknum02'].AddItem(str(i))  # 将轨道数量添加到轨道数下拉框中
 
 
fu = get_fusion()
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
clip_colors = ['Orange_橘黄', 'Apricot_杏黄', 'Yellow_黄色', 'Lime_黄绿', 'Olive_墨绿', 'Green_绿色',
               'Teal_蓝绿', 'Navy_深蓝', 'Blue_蓝色', 'Purple_紫色', 'Violet_紫红', 'Pink_粉红',
               'Tan_浅棕', 'Beige_米黄', 'Brown_棕色', 'Chocolate_深棕']
window_01 = [  # 定义窗口布局，包含一个水平容器（HGroup）
    ui.HGroup({"Spacing": 10},  # 创建一个水平布局容器，设置控件之间的间距为10
    [
        ui.VGroup({"Spacing": 10}, [  # 创建一个垂直布局容器，设置控件之间的间距为10
            # ui.HGap({"Spacing": 0.3}),  # 创建水平间隔控件，间距为10
            # ui.Label({"ID": 'label_01', "Text": "将指定颜色的镜头添加到时间线末尾",}),  # 创建标签控件，显示说明文本
            ui.HGap({"Spacing": 10}),  # 创建水平间隔控件，间距为10
 
            ui.HGroup({"Spacing": 10}, [  # 创建一个水平容器，包含下拉框和刷新按钮，控件间隔为10
                ui.LineEdit({"ID": "r_path0002", "PlaceholderText": "模板路径（如不导入模板则按默认样式转换）",'ClearButtonEnabled': True }),
                ui.Button({ "ID": "pickpath0002", "Text": "导入模板","Weight": 0.3})
            ]),
            ui.Label({"ID": 'label_03', "Text": "选择字幕轨道",}),  # 创建标签控件，显示说明文本
            ui.HGroup({"Spacing": 10}, [  # 创建一个水平容器，包含下拉框和刷新按钮，控件间隔为10
                ui.ComboBox({"ID": "tracknum02", "Weight": 7}),  # 创建一个下拉框控件，供用户选择视频轨道数量，权重为7
                ui.Button({"ID": "refresh_track02","Text": "刷新"}),  # 创建一个按钮控件，显示文本为“刷新”
            ]),
            ui.Label({"ID": 'label_04', "Text": "选择视频轨道（必须为空白轨道）",}),  # 创建标签控件，显示说明文本
            ui.HGroup({"Spacing": 10}, [  # 创建一个水平容器，包含下拉框和刷新按钮，控件间隔为10
                ui.ComboBox({"ID": "tracknum", "Weight": 7}),  # 创建一个下拉框控件，供用户选择视频轨道数量，权重为7
                ui.Button({"ID": "refresh_track","Text": "刷新"}),  # 创建一个按钮控件，显示文本为“刷新”
            ]),
            ui.HGap({"Spacing": 10}),  # 创建水平间隔控件，间距为10
            ui.Button({"ID": "add_job", "Text": "添加到视频轨道", "Enabled": True,"Default": True,"Weight": 1.5}),  # 创建一个按钮控件，显示“Run”，并禁用
            # ui.HGap({"Spacing": 5}),  # 创建水平间隔控件，间距为10
            # ui.Label({"ID": 'label_02', "Text": "翻译后添加","Font": ui.Font({ 'PointSize': 10 }),"Font": ui.Font({ 'PointSize': 12 }),'Alignment': { 'AlignCenter' : True }}),  # 创建另一个标签控件，显示说明文本
            ui.HGroup({"Spacing": 10}, [
                ui.Button({"ID": "AAF", "Text": "英文>>中文_翻译添加","Weight": 1.3}),  # 创建一个按钮控件，显示“Run”，并禁用
                ui.Button({"ID": "EDL", "Text": "中文>>英文_翻译添加","Weight": 1.3}),
            ]),
            ui.HGap({"Spacing": 10}),  # 创建水平间隔控件，间距为10
            ui.Label({"ID": 'label_53', "Text": "文字替换", }),  # 创建标签控件，显示说明文本
            ui.HGroup({"Spacing": 10}, [  # 创建一个水平容器，包含下拉框和刷新按钮，控件间隔为10
                ui.LineEdit({"ID": "yuanlai", "PlaceholderText": "输入需替换文字"}),
                ui.Label({"ID": 'label_025', "Text": "          替换成", }),  # 创建标签控件，显示说明文本
                ui.LineEdit({"ID": "tihuan", "PlaceholderText": ""}),
                ui.Button({ "ID": "tihuananniu", "Text": "确认替换", "Weight": 0.5})
            ]),
            ui.HGap({"Spacing": 10}),  # 创建水平间隔控件，间距为10
            ui.Label({"ID": 'label_02', "Text": "基于当前选择的视频轨道导出SRT文件","Font": ui.Font({ 'PointSize': 10 }),"Font": ui.Font({ 'PointSize': 12 }),'Alignment': { 'AlignCenter' : True }}),  # 创建另一个标签控件，显示说明文本
            ui.HGroup({"Spacing": 10}, [  # 创建一个水平容器，包含下拉框和刷新按钮，控件间隔为10
                ui.LineEdit({"ID": "r_path", "PlaceholderText": "不导出SRT时无需输入此选项"}),
                ui.Button({ "ID": "pickpath", "Text": "选择路径","Weight": 0.3})
            ]),
            # ui.HGap({"Spacing": 10}),  # 创建水平间隔控件，间距为10
            ui.Button({"ID": "add_job022", "Text": "SRT导出", "Enabled": False,"Default": True,"Weight": 1.5}),  # 创建一个按钮控件，显示“Run”，并禁用
            ui.HGap({"Spacing": 10}),  # 创建水平间隔控件，间距为10
 
            ui.HGroup({"Spacing": 10}, [  # 创建一个水平容器，包含下拉框和刷新按钮，控件间隔为10
                ui.LineEdit({"ID": "r_path02", "PlaceholderText": "输入需要翻译的文字"}),
                ui.Button({ "ID": "fanyi01", "Text": "翻译", "Weight": 0.3})
            ]),
            ui.TextEdit({"ID": "r_path022", 'WordWrap': True,"Weight": 4}),
 
            ui.Label({"ID": 'label_03', "Text": "@更多工具可关注B站:刘榕易",'Alignment': { 'AlignCenter' : True }}),  # 创建另一个标签控件，显示说明文本
 
            ui.HGap({"Spacing": 10}),  # 创建水平间隔控件，间距为10
        ]),
    ]),
]
 
current_window = window_01  # 将当前窗口设置为定义的窗口布局
 
 
dlg = disp.AddWindow({  # 创建窗口
    "WindowTitle": "达芬奇_字幕先生",  # 设置窗口标题
    "ID": "MyWin",  # 设置窗口ID
    "Geometry": [  # 设置窗口的位置和大小
        700, 300,  # 窗口初始位置 (x, y)
        500, 680  # 窗口宽度和高度
    ],
}, current_window)  # 使用之前定义的布局作为窗口内容
 
itm = dlg.GetItems()  # 获取窗口中的所有控件项
load_track_count()  # 加载轨道数
load_track_count02()
def _func(ev):  # 定义窗口关闭事件的处理函数
    disp.ExitLoop()  # 退出事件循环
dlg.On.MyWin.Close = _func  # 将关闭窗口时触发的事件与 _func 函数绑定
 
def _refresh_track(ev):  # 定义点击“刷新轨道数”按钮时执行的函数
    load_track_count()  # 重新加载轨道数
def _refresh_track02(ev):  # 定义点击“刷新轨道数”按钮时执行的函数
    load_track_count02()  # 重新加载轨道数
 
def _run_add(ev):  # 定义点击“Run”按钮时执行的函数
    global track
    global track02
    track = int(itm['tracknum'].CurrentText)  # 获取当前选择的视频轨道数
    track02 = int(itm['tracknum02'].CurrentText)  # 获取当前选择的视频轨道数
    # print(track02)
    # print(track)
 
    aDD_timeline()
    itm['r_path022'].Text = "字幕转换已经完成！！！"
def _run_add02(ev):  # 定义点击“Run”按钮时执行的函数
    global track
    global track02
    track = int(itm['tracknum'].CurrentText)  # 获取当前选择的视频轨道数
    track02 = int(itm['tracknum02'].CurrentText)  # 获取当前选择的视频轨道数
    # print(track02)
    # print(track)
    if __name__ == '__main__':
        itm['r_path022'].Text = "初始化完成，请再次点击！"
        aDD_timelineZH()
        itm['r_path022'].Text = "字幕转换已经完成！！！"
 
 
 
 
 
 
def fanyi():
    global fanyi22Text
    from googletrans import Translator
    translator = Translator()
    tx = itm['r_path02'].GetText()  # 获取渲染路径文本框中的文本
    # if len(itm['r_path02'].Text) >= 1:
    #     itm['fanyi01'].Enabled = True
    # else:
    #     itm['fanyi01'].Enabled = False
    detected = translator.detect(tx)
    yuyan = detected.lang
    if yuyan == 'zh-CN':
        translated = translator.translate(tx, src='zh-cn', dest='en')
        fanyi22Text = translated.text  # 设置文本内容
    if yuyan == 'en':
        translated = translator.translate(tx, src=yuyan, dest='zh-cn')
        fanyi22Text = translated.text  # 设置文本内容
    else:
        print("无法识别该语言")
    print(yuyan)
 
 
def _run_add03(ev):  # 定义点击“Run”按钮时执行的函数
    global track
    global track02
    track = int(itm['tracknum'].CurrentText)  # 获取当前选择的视频轨道数
    track02 = int(itm['tracknum02'].CurrentText)  # 获取当前选择的视频轨道数
    # print(track02)
    # print(track)
    if __name__ == '__main__':
        itm['r_path022'].Text = "初始化完成，请再次点击！"
        aDD_timelineEN()
        itm['r_path022'].Text = "字幕转换已经完成！！！"
def _run_add04(ev):  # 定义点击“Run”按钮时执行的函数
    global track
    global track02
    global path
    path = itm['r_path'].GetText()  # 获取渲染路径文本框中的文本
    track = int(itm['tracknum'].CurrentText)  # 获取当前选择的视频轨道数
    track02 = int(itm['tracknum02'].CurrentText)  # 获取当前选择的视频轨道数
 
    # print(track02)
    # print(track)
    ouputSRT()
    itm['r_path022'].Text = "SRT字幕导出已经完成！！！"
 
def _run_add05(ev):
    fanyi()
    itm['r_path022'].Text =fanyi22Text
 
    print("字幕翻译完成")
def _pickfile(ev):  # 定义文件选择函数
    global selected
    selected = fu.RequestDir()  # 弹出文件选择对话框，让用户选择目录
    itm['r_path'].Text = str(selected)  # 设置渲染路径文本框为用户选择的路径
    if len(itm['r_path'].Text) >= 1:
        itm['add_job022'].Enabled = True
    else:
        itm['add_job022'].Enabled = False
    return selected  # 返回选择的路径
def _pickfile0002(ev):  # 定义文件选择函数
    global selected02
    selected02 = fu.RequestFile() # 弹出文件选择对话框，让用户选择目录
    itm['r_path0002'].Text = str(selected02)  # 设置渲染路径文本框为用户选择的路径
    return selected02  # 返回选择的路径
 
dlg.On.pickpath.Clicked = _pickfile
dlg.On.pickpath0002.Clicked = _pickfile0002
 
dlg.On.refresh_track.Clicked = _refresh_track  # 绑定“刷新轨道数”按钮点击事件
dlg.On.refresh_track02.Clicked = _refresh_track02  # 绑定“刷新轨道数”按钮点击事v
dlg.On.add_job.Clicked = _run_add # 绑定“刷新轨道数”按钮点击事件
dlg.On.AAF.Clicked = _run_add02 # 绑定“刷新轨道数”按钮点击事件
dlg.On.EDL.Clicked = _run_add03 # 绑定“刷新轨道数”按钮点击事件
dlg.On.add_job022.Clicked = _run_add04 # 绑定“刷新轨道数”按钮点击事件
dlg.On.fanyi01.Clicked = _run_add05 # 绑定“刷新轨道数”按钮点击事件
dlg.On.tihuananniu.Clicked = tihuanzimu # 绑定“刷新轨道数”按钮点击事件
 
if __name__ == "__main__":  # 如果该脚本是主程序执行
    dlg.Show()  # 显示窗口
    disp.RunLoop()  # 启动事件循环
    dlg.Hide()  # 隐藏窗口