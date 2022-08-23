from PIL import Image
import numpy as np
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description="A tool of LSB steganography")
parser.add_argument("-w", "--write", action="store_true", help="隐写模式")
parser.add_argument("-r", "--read", action="store_true", help="读取模式")
parser.add_argument("--red", action="store_true", help="隐写于红色通道")
parser.add_argument("--green", action="store_true", help="隐写于绿色通道")
parser.add_argument("--blue", action="store_true", help="隐写于蓝色通道")
parser.add_argument("-i", "--input", nargs="+", required=True, help="输入路径")
parser.add_argument("-o", "--output", nargs=1, default="output.png", help="输出路径")
args = vars(parser.parse_args())
# print(args)
# exit()
if args["write"] and args["read"]:
    raise RuntimeError("Arguments -w(--write) and -r(--read) can't coexist.")
if not args["write"] and not args["read"]:
    raise RuntimeError("Need a mode argument, such as -r or -w.")
if args["red"] + args["green"] + args["blue"] == 0:
    raise RuntimeError("Need a color channel argument, such as --red, --green or --blue.")
if args["red"] + args["green"] + args["blue"] > 1:
    raise RuntimeError("Arguments --red, --green and --blue can't coexist.")
if args["write"] and len(args["input"]) < 2:
    raise "Write mode need 2 pictures as input. Received 1."

color_channel = "r"
color_channel = "g" if args["green"] else color_channel
color_channel = "b" if args["blue"] else color_channel


def set_one(num):
    return num | 0b00000001


def set_zero(num):
    return num & 0b11111110


def get_last(num):
    return num & 0b00000001


def write(surface, shadow, channel):
    if channel == "r":
        channel = 0
    elif channel == "g":
        channel = 1
    elif channel == "b":
        channel = 2
    surface = np.array(surface)
    shadow = shadow.convert("L")
    shadow = np.array(shadow)
    assert surface.shape[0] > shadow.shape[0], "surface picture's width must large than shadow picture's"
    assert surface.shape[1] > shadow.shape[1], "surface picture's height must large than shadow picture's"
    width = shadow.shape[0]
    height = shadow.shape[1]
    for i in tqdm(range(width)):
        for j in range(height):
            if shadow[i][j] > 127:
                surface[i][j][channel] = set_one(surface[i][j][channel])
            else:
                surface[i][j][channel] = set_zero(surface[i][j][channel])
    surface = Image.fromarray(surface)
    return surface


def read(surface, channel):
    if channel == "r":
        channel = 0
    elif channel == "g":
        channel = 1
    elif channel == "b":
        channel = 2
    surface = np.array(surface)
    width = surface.shape[0]
    height = surface.shape[1]
    result = []
    for i in tqdm(range(width)):
        tmp = []
        for j in range(height):
            tmp.append(255 if get_last(surface[i][j][channel]) == 1 else 0)
        result.append(tmp)
    result = np.array(result)
    result.reshape((result.shape[0], result.shape[1], 1))
    result = Image.fromarray(result)
    return result


if args["write"]:
    print("Write mode")
    pic1 = Image.open(args["input"][0])
    pic2 = Image.open(args["input"][1])
    pic2 = pic2.convert("L")
    res_img = write(pic1, pic2, color_channel)
    res_img.save(args["output"])

if args["read"]:
    print("Read mode")
    pic1 = Image.open(args["input"][0])
    res_img = read(pic1, color_channel)
    res_img = res_img.convert("RGB")
    res_img.save(args["output"][0])
