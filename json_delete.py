import json

def delete_track_id(json_file, track_id):
    # 读取json文件
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 遍历json文件的每一个元素
    for frame in list(data['frames'].keys()):
        for obj in list(data['frames'][frame]['cv_annotation'].keys()):
            # 检查"track_id"是否等于输入的整数
            if data['frames'][frame]['cv_annotation'][obj]['track_id'] == str(track_id):
                # 如果等于，删除这个元素
                del data['frames'][frame]['cv_annotation'][obj]

    # 将修改后的数据写回json文件
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

# 使用示例
delete_track_id('C:/codefield/code_p/Yolov5_DeepSort_Pytorch-master/Yolov5_DeepSort_Pytorch-master/images/json/a_1.json', 58)