import os.path

from scapy.all import rdpcap
import numpy as np
from PIL import Image

# 读取pcap文件并提取字节流
def pcap2bytes(pcap_file,max_len=784): # 默认最大长度为784,即28*28,用于确定图片大小
    packets = rdpcap(pcap_file)
    bytes_list = []

    # 提取字节流
    for packet in packets:
        raw_bytes=bytes(packet) # 将数据包转换为字节序列
        # print("raw_bytes:",raw_bytes)
        print("len(raw_bytes):",len(raw_bytes))
        print("===============================")
        byte_array=list(raw_bytes)
        if len(byte_array)<max_len//2:
            continue
        # 如果数据包长度小于最大长度，则在末尾补0;如果数据包长度大于最大长度，则截断
        if len(byte_array)<max_len:
            byte_array+=[0]*(max_len-len(byte_array))
        else:
            byte_array=byte_array[:max_len]
        bytes_list.append(byte_array)
    return bytes_list

# 将一个数据包的字节流转换为图片并保存
def bytes2image(byte_list,image_name):
    # 将一维的字节流转换为二维的灰度图
    img=np.array(byte_list).reshape(28,28)
    img=Image.fromarray(img.astype(np.uint8)) # 将numpy数组转换为PIL图像
    img.save(image_name)

#将每张图片保存到本地
def save_images(bytes_list):
    for idx,byte_list in enumerate(bytes_list):
        image_name=os.path.join("./mdata/video_streaming",f"image_{idx}.png")
        bytes2image(byte_list,image_name)
        print(f"Save {image_name} successfully!")

# 读取pcap文件并提取字节流
pcap_file="./Tor-nonTor/video_streaming/VIDEO_Youtube_HTML5_Gateway.pcap"
bytes_list=pcap2bytes(pcap_file)
# 将每张图片保存到本地
save_images(bytes_list)


