import os
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CHARACTERS = string.ascii_letters + string.digits

def get_random_font(font_directory):
  """Get a random font path from, a specific directory"""
  if not os.path.exists(font_directory):
    raise Exception("Font directory does not exist")
  if not os.listdir(font_directory):
    raise Exception("Font directory is empty")
  font_files = [f for f in os.listdir(font_directory) if f.lower().endswith((".ttf", "otf"))]
  if not font_files:
    raise Exception("No font files found in font directory")
  return os.path.join(font_directory, random.choice(font_files))

def random_color(min_val, max_val):
  """Get a random color"""
  return (random.randint(min_val, max_val), random.randint(min_val, max_val), random.randint(min_val, max_val))

def add_noise_dots(draw, width, height, num_dots_factor = 0.01):
  """Add noise dots to the image"""
  nums_dots = int(width * height * num_dots_factor)
  for _ in range(nums_dots):
      draw.point((random.randint(0, width-1), random.randint(0, height-1)), fill=random_color(0,200))

def add_noise_lines(draw, width, height, num_lines_factor = 0.0001):
  """Add noise lines to the image"""
  num_lines = int(width * height * num_lines_factor)
  for _ in range(num_lines):
      x1 = random.randint(0, width-1)
      y1 = random.randint(0, height-1)
      x2 = random.randint(0, width-1)
      y2 = random.randint(0, height-1)
      draw.line((x1, y1, x2, y2), fill=random_color(0,220), width=random.randint(1, 2))

def generate_random_text(length_min, length_max):
  """Generate a random text"""
  length = random.randint(length_min, length_max)
  return "".join(random.choices(CHARACTERS, k=length))


def create_CAPTCHA(image_width, image_height, font_size_min, font_size_max, text_length_min, text_length_max, font_directory):
  """Create a CAPTCHA and return a PIL image and the text assiociated"""

  captcha_text = generate_random_text(text_length_min, text_length_max) #text_generation
  font_path = get_random_font(font_directory) #font_generation
  font_size = random.randint(font_size_min, font_size_max) #font_size_generation
  try :
    font = ImageFont.truetype(font_path, font_size)
  except :
    font = ImageFont.load_default()
    print(f"Error while loading font {font_path}, using default font")

  image = Image.new("RGB", (1,1))
  dummy_draw = ImageDraw.Draw(image)

  text_bbox_unrotated = dummy_draw.textbbox((0,0), captcha_text, font=font)
  text_width = text_bbox_unrotated[2] - text_bbox_unrotated[0]
  text_height = text_bbox_unrotated[3] - text_bbox_unrotated[1]

  padding = int(font_size*0.8)
  text_layer_width = text_width + 2*padding
  text_layer_height = text_height + 2*padding

  text_layer = Image.new("RGBA",(text_layer_width, text_layer_height), (0,0,0,0))
  text_layer_draw = ImageDraw.Draw(text_layer)
  draw = ImageDraw.Draw(image)

  text_color = random_color(0,150)
  text_layer_draw.text((padding, padding), captcha_text, font=font, fill=text_color)

  num_strikethrough_lines = random.randint(1, 2)
  for _ in range(num_strikethrough_lines):
        line_thickness = random.randint(font_size // 15, font_size // 10) # Épaisseur relative à la taille de la police
        if line_thickness < 1 :
          line_thickness = 1
        line_color_val = random_color(0, 120)

        # Coordonnées Y de la ligne par rapport au texte dans text_layer
        # Le texte commence à y=padding et a une hauteur text_height_unrotated
        line_y_rel_to_text = random.uniform(0.3, 0.7) # Position en % de la hauteur du texte
        line_y_abs = padding + int(text_height * line_y_rel_to_text)

        # Permettre à la ligne d'avoir un léger angle par rapport à l'horizontale du texte
        angle_offset_y = random.randint(-int(text_height * 0.15), int(text_height * 0.15))

        # La ligne doit couvrir le texte horizontalement
        start_x = padding - random.randint(0, int(padding * 0.3)) # Commence un peu avant le texte
        end_x = padding + text_width + random.randint(0, int(padding * 0.3)) # Finit un peu après

        text_layer_draw.line(
            [(start_x, line_y_abs - angle_offset_y), (end_x, line_y_abs + angle_offset_y)],
            fill=line_color_val,
            width=line_thickness)

  angle = random.uniform(-80, 80) # Plage de rotation augmentée
  rotated_text_layer = text_layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC, fillcolor=(0,0,0,0))
  rotated_width = rotated_text_layer.width
  rotated_height = rotated_text_layer.height


  background_color = random_color(150, 255)
  final_image = Image.new("RGB", (image_width, image_height), background_color)
  final_draw = ImageDraw.Draw(final_image)

  add_noise_dots(final_draw, image_width, image_height)
  add_noise_lines(final_draw, image_width, image_height)

  if rotated_width < image_width :
    paste_x = random.randint(0, image_width - rotated_width)
  else:
    paste_x = 0

  if rotated_height < image_height :
    paste_y = random.randint(0, image_height - rotated_height)
  else:
    paste_y = 0

  final_image.paste(rotated_text_layer, (paste_x, paste_y), rotated_text_layer)

  return final_image, captcha_text


