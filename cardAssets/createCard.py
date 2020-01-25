from PIL import Image, ImageDraw, ImageFont
import requests

def createCard(upvotes,downvotes,name,avatar_url):
    karma = upvotes-downvotes
    red_x1,red_y1,red_x2,red_y2 = 294,113,646,159
    bar_size = [red_x2-red_x1,red_y2-red_y1]
    
    total_vote = upvotes+downvotes
    upvote_percentage = (upvotes/total_vote)

    img = Image.open("template.png")
    canvas = Image.new('RGBA', (700, 250), (0, 0, 0, 0))
    canvas.paste(img, (0,0))

    rimg_draw = ImageDraw.Draw(canvas)
    rimg_draw.rectangle((red_x1,red_y1,red_x2,red_y2), "#FF463D")

    green_x2 = red_x1+(bar_size[0]*upvote_percentage)
    rimg_draw.rectangle((red_x1,red_y1,green_x2,red_y2), "#70FF32")

    img = Image.open("bar_overlay.png").convert("RGBA")
    canvas.paste(img, (0, 0), img)

    img = Image.open(requests.get(avatar_url, stream=True).raw)
    size = 226, 226
    img.thumbnail(size)
    canvas.paste(img, (15,12))

    img = Image.open("circle_overlay.png").convert("RGBA")
    canvas.paste(img, (0,0), img)
    
###########################################################################
    
    W, H = (352,46)
    if karma>0:
        karma = "+"+str(karma)
    
    msg = f"{name}        {karma}"

    arial_font = ImageFont.truetype('arial.ttf', 40)
    rimg_draw.text((294, 60),f"{name} {karma}","#CECECE",font=arial_font)

    karma_coords = (294,168)
    arial_font = ImageFont.truetype('arial.ttf', 12)
    rimg_draw.text(karma_coords,f"{upvotes}","#70FF32",font=arial_font)
    size_of_text = arial_font.getsize(f"{upvotes}")

    karma_coords = list(karma_coords)
    karma_coords[0] += size_of_text[0]
    karma_coords = tuple(karma_coords)
    rimg_draw.text(karma_coords,f"|","#CECECE",font=arial_font)
    size_of_text = arial_font.getsize(f"|")
    
    karma_coords = list(karma_coords)
    karma_coords[0] += size_of_text[0]
    karma_coords = tuple(karma_coords)
    rimg_draw.text(karma_coords,f"{downvotes}","#FF463D",font=arial_font)

    canvas.save("card.png")


createCard(106,23,"sarim","https://cdn.discordapp.com/avatars/297111993352060948/4109edce51d37d9ede756bea4e8059e9.jpg?size=1024")

