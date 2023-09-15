import qrcode

# 创建QRCode对象
qr = qrcode.QRCode(version=1, box_size=10, border=5)

# 设置二维码数据
data = 'https://www.baidu.com'
qr.add_data(data)

# 填充数据并生成二维码
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

# 保存二维码图片
img.save("qrcode.png")