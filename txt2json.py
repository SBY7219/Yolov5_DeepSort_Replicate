import json

def parse_line(line):
    """将一行文本转换为数据字典"""
    parts = line.strip().split()
    frame_id, track_id, x, y, width, height = map(int, parts[:6])
    return {
        'frame_id': frame_id,
        'track_id': track_id,
        'bbox': [x, y, x + width, y + height]  # 转换为对角坐标格式
    }

def convert_to_json(input_file, video_name):
    # 初始化数据结构，用于存储最终的结果
    data = {
        'video_name': video_name,
        'frames': {}
    }
    # 初始化一个字典，用于跟踪每个对象的出现帧
    track_frames = {}

    with open(input_file, 'r') as file:
        for line in file:
            parsed = parse_line(line)
            frame_id = parsed['frame_id']
            track_id = parsed['track_id']
            bbox = parsed['bbox']

            frame_key = f'frame_{frame_id}'
            track_key = f'objType_track_{track_id}'

            # 更新track_frames字典，记录track_id出现在哪些frame_id中
            if track_id not in track_frames:
                track_frames[track_id] = []
            track_frames[track_id].append(frame_id)

            # 如果当前帧还没有被记录在data中，则添加
            if frame_key not in data['frames']:
                data['frames'][frame_key] = {'cv_annotation': {}}

            # 更新或创建track_id对应的追踪信息
            data['frames'][frame_key]['cv_annotation'][track_key] = {
                'object_type': 'pedestrian',  # 实际对象类型未知，根据需求更改
                'track_id': str(track_id),
                'bbox': bbox,
                'observed_frames': []
            }

    # 填充每个track_id的observed_frames
    for frame_data in data['frames'].values():
        for track_key, track_info in frame_data['cv_annotation'].items():
            track_id = int(track_info['track_id'])
            track_info['observed_frames'] = track_frames[track_id]

    return json.dumps(data, indent=4)

def save_json_to_file(json_str, output_file):
    """将JSON字符串保存到文件"""
    with open(output_file, 'w') as file:
        file.write(json_str)

# 指定输入文件和视频名称
input_file = 'C:/codefield/code_p/Yolov5_DeepSort_Pytorch-master/Yolov5_DeepSort_Pytorch-master/inference/output/a.txt'
video_name = 'C:/codefield/code_p/Yolov5_DeepSort_Pytorch-master/Yolov5_DeepSort_Pytorch-master/images/images/a.mp4'
# 指定输出JSON文件的路径
output_json_file = 'C:/codefield/code_p/Yolov5_DeepSort_Pytorch-master/Yolov5_DeepSort_Pytorch-master/images/json/a.json'
# 转换JSON并保存到文件
json_output = convert_to_json(input_file, video_name)
save_json_to_file(json_output, output_json_file)

print(f"JSON output has been saved to {output_json_file}")
