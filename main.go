package main

import (
	"encoding/binary"
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
)

const CHN_NUM = 4
const WIDTH = 2

var FrameLen = CHN_NUM * WIDTH

type ChannelVib struct {
	CHData [4][]byte
}

func parseData(rawData []byte, vibdata []byte) ([]byte, []byte) {
	buffer := rawData
	buffer = buffer[2:]
	bufferLenByte := buffer[:2]
	buffer = buffer[2:]
	length := binary.BigEndian.Uint16(bufferLenByte)
	d := buffer[:length]
	buffer = buffer[length:]
	vibrateBuffer := d[3 : len(d)-1]
	vibdata = append(vibdata, vibrateBuffer...)
	rawData = buffer
	return rawData, vibdata
}

func splitIntoChannel(vibrateBuffer []byte) *ChannelVib {
	channelData := new(ChannelVib)
	for i := 0; i < len(vibrateBuffer); i += FrameLen {
		channelData.CHData[0] = append(channelData.CHData[0], vibrateBuffer[i:i+2]...)
		channelData.CHData[1] = append(channelData.CHData[1], vibrateBuffer[i+2:i+4]...)
		channelData.CHData[2] = append(channelData.CHData[2], vibrateBuffer[i+4:i+6]...)
		channelData.CHData[3] = append(channelData.CHData[3], vibrateBuffer[i+6:i+8]...)
	}
	return channelData
}

func ReadBuffer(filename string) {
	fd, err := os.OpenFile(filename, os.O_RDONLY, 0777)
	if err != nil {
		fmt.Println(err)
		return
	}
	fileData, err := io.ReadAll(fd)
	if err != nil {
		fmt.Println(err)
		return
	}
	buffer := make([]byte, 0)
	fmt.Println(len(fileData))
	for {
		fileData, buffer = parseData(fileData, buffer)
		if len(fileData) == 0 {
			break
		}
	}
	fmt.Println(len(buffer))

	result := splitIntoChannel(buffer)
	for k, v := range result.CHData {
		fd, err = os.Create(strconv.Itoa(k))
		if err != nil {
			fmt.Println(err)
			return
		}
		_, err = fd.Write(v)
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}

func main() {
	startTime := time.Now().UnixMilli()
	ReadBuffer("1700806843-55552")
	fmt.Println(time.Now().UnixMilli() - startTime)
}
