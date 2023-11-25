import struct
import time

# 对二进制数据的读取和解析


CHANNEL_NUM=4
WIDTH = 2
# LENGTH = 1028
# STATIC_TCP_FRAME = 1028+4
channel_dict = {
    0:b'',
    1:b'',
    2:b'',
    3:b'',
}

def parse_binary_bffer(raw_data:bytes, binary_data:bytes):
    buffer = raw_data
    buffer = buffer[2:]
    # 前两个字节无意义

    data_package_len = struct.unpack('>H',buffer[:2])[0]
    # 第三第四字节是包长度
    buffer = buffer[2:]

    data_package = buffer[:data_package_len]
    # 取得数据包内容
    buffer = buffer[data_package_len:]

    binary_data += data_package[3:-1]
    # 包内容的最后一个字节是占位符，前三字节也是占位符

    return buffer, binary_data

def get_channel_data(binary_data):
    frame_len = WIDTH*CHANNEL_NUM
    channel_dict[0]=b''.join([binary_data[i:i+frame_len][:2] for i in range(0,len(binary_data),frame_len)])
    channel_dict[1]=b''.join([binary_data[i:i+frame_len][2:4] for i in range(0,len(binary_data),frame_len)])
    channel_dict[2]=b''.join([binary_data[i:i+frame_len][4:6] for i in range(0,len(binary_data),frame_len)])
    channel_dict[3]=b''.join([binary_data[i:i+frame_len][6:8] for i in range(0,len(binary_data),frame_len)])


def read_package(filename):
    # cnt = 0
    # binary_data = b''.join([raw_data[i+2+2+3:i+2+2+LENGTH-1] for i in range(0,len(raw_data),STATIC_TCP_FRAME)])
    raw_data = open(filename,"rb").read()
    binary_data = b''
    print(len(raw_data))
    while len(raw_data) > 0:
        raw_data,binary_data = parse_binary_bffer(raw_data,binary_data)
    print(len(binary_data))
    get_channel_data(binary_data)
    for k,v in channel_dict.items():
        print(k,len(v))
        open('%s'%k,'wb').write(v)



if __name__ == '__main__':
    start_time = int(time.time()*1000)
    filename = "1700806843-55552"
    read_package(filename)
    print(int(time.time()*1000)-start_time)








