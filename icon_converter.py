from PIL import Image

img = Image.open("Group 10.png").convert("RGBA")

# 推荐尺寸：确保图标清晰且兼容多平台
img = img.resize((256, 256))

# 保存 .ico，保持透明背景
img.save("icon_crystal.ico", format='ICO', sizes=[(256, 256)])
