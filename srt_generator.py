def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def split_text_by_punctuation(full_text):
    """按标点将原文拆分成句子片段"""
    sentence_end = set('。！？.')
    pause_marks = set('，；、：,;')
    all_breaks = sentence_end | pause_marks

    segments = []
    current = ""

    for ch in full_text:
        current += ch
        if ch in all_breaks:
            segments.append(current)
            current = ""

    if current.strip():
        segments.append(current)

    return segments

def strip_punctuation(text):
    """去掉文本中的标点和空白"""
    sentence_end = set('。！？.')
    pause_marks = set('，；、：,;')
    all_breaks = sentence_end | pause_marks
    return "".join(ch for ch in text if ch not in all_breaks and ch not in ' \n\t')

def group_items_into_sentences(items, full_text):
    if not items:
        return []

    all_item_text = "".join(it.text for it in items)
    segments = split_text_by_punctuation(full_text)

    sentences = []
    item_pos = 0  # 当前搜索位置（在all_item_text中）

    for seg in segments:
        seg_stripped = strip_punctuation(seg)
        if not seg_stripped:
            continue

        # 在all_item_text中找到这个片段
        found_pos = all_item_text.find(seg_stripped, item_pos)

        if found_pos == -1:
            # 匹配失败，跳过
            continue

        # 找到起始item
        char_count = 0
        start_item = 0
        for i, item in enumerate(items):
            if char_count + len(item.text) > found_pos:
                start_item = i
                break
            char_count += len(item.text)

        # 找到结束item
        end_pos = found_pos + len(seg_stripped)
        end_item = start_item
        for i in range(start_item, len(items)):
            end_item = i
            if char_count >= end_pos:
                break
            char_count += len(items[i].text)

        # 更新搜索位置
        item_pos = found_pos + len(seg_stripped)

        # 去掉末尾标点
        display_text = seg.strip()
        sentence_end = set('。！？.')
        pause_marks = set('，；、：,;')
        while display_text and display_text[-1] in sentence_end | pause_marks:
            display_text = display_text[:-1]

        sentences.append({
            "text": display_text,
            "start": items[start_item].start_time,
            "end": items[end_item].end_time
        })

    return sentences

def timestamps_to_srt(timestamps, text, output_path):
    if timestamps is None:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("")
        return

    items = None
    if hasattr(timestamps, 'items'):
        items = timestamps.items
    elif hasattr(timestamps, '__len__') and len(timestamps) > 0:
        first = timestamps[0]
        if hasattr(first, 'items'):
            items = first.items
        elif hasattr(first, 'text') and hasattr(first, 'start_time'):
            items = timestamps

    if not items:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("")
        return

    sentences = group_items_into_sentences(items, text)

    lines = []
    for i, sent in enumerate(sentences, 1):
        start = format_time(sent["start"])
        end = format_time(sent["end"])
        lines.append(f"{i}\n{start} --> {end}\n{sent['text']}\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
