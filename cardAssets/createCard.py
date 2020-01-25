from PIL import Image

def createCard(upvotes,downvotes,name,profile_picture):
    img = Image.open("template.png")
    canvas = Image.new('RGBA', (700, 250), (0, 0, 0, 0))
    canvas.paste(img, (0,0))
    canvas.show()

createCard(0,0,0,0)

