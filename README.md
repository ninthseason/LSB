# LSB-Steganography

LSB 隐写术的命令行实现

## 使用方法

```shell
# 隐写
python LSB.py -w --red -i pic1.png pic2.png -o result.png
```

```shell
# 读取
python LSB.py -r --red -i result.png -o res2.png
```

## 注意点

1. 表图像尺寸必须大于里图像

2. 表图像可以是彩色图像，里图像会被二值化

3. 输出格式必须为 png 或 bmp

4. 理论上因为 RGB 三个通道每像素共能隐写 3 比特信息，本程序仅实现了单通道隐写


