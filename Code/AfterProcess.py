import os


def remove_think_tags(text):
    current_start = 0
    n = len(text)
    while current_start < n:
        # 查找下一个 <think> 标签
        start_index = text.find('<think>', current_start)
        if start_index == -1:
            break  # 没有更多开标签，退出

        count = 1
        temp_index = start_index + 7  # 跳过当前 <think>
        end_index = -1

        # 扫描以找到匹配的闭合标签
        while temp_index < n and count > 0:
            next_open = text.find('<think>', temp_index)
            next_close = text.find('</think>', temp_index)

            # 检查是否找到标签
            if next_open == -1 and next_close == -1:
                break  # 没有更多标签

            # 确定下一个标签是开标签还是闭标签
            if next_open != -1 and (next_close == -1 or next_open < next_close):
                # 遇到开标签：增加计数并跳过
                count += 1
                temp_index = next_open + 7
            else:
                # 遇到闭标签：减少计数
                count -= 1
                if count == 0:
                    end_index = next_close  # 记录匹配的闭合标签位置
                temp_index = next_close + 7  # 跳过当前 </think>

        if end_index == -1:
            # 未找到匹配的闭合标签：跳过当前开标签
            current_start = start_index + 7
        else:
            # 删除匹配的标签对及其内容
            text = text[:start_index] + text[end_index + 7:]
            # 重置扫描位置（文本已改变）
            current_start = 0
            n = len(text)  # 更新文本长度

    return text


for root, dirs, files in os.walk('..\Data\CleanExtractResult'):
    for file in files:
        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
            text = f.read().strip("\"")
        text = remove_think_tags(text)
        text = text.replace('\\n\\n','\\n').replace('*',"").replace('\\','')
        text = text.split('\\n')
        with open(os.path.join(root, file), 'w', encoding='utf-8') as f:
            for line in text:
                f.write(line+'\n')
