import os
import random
import json
from PIL import Image, ImageDraw, ImageFont
from pycocotools.coco import COCO
import requests, zipfile, os
from io import BytesIO

# Crée le dossier cible
os.makedirs('data/coco2017', exist_ok=True)

# Télécharge et extrait les annotations
ann_url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
r = requests.get(ann_url)
with zipfile.ZipFile(BytesIO(r.content)) as z:
    z.extractall('data/coco2017')

# Télécharge et extrait les images d'entraînement
img_url = 'http://images.cocodataset.org/zips/train2017.zip'
r = requests.get(img_url)
with zipfile.ZipFile(BytesIO(r.content)) as z:
    z.extractall('data/coco2017/train2017')

print("COCO 2017 téléchargé dans data/coco2017") 

# --- CONFIGURATION ---
DATA_DIR   = 'data/coco2017'
IMG_DIR    = os.path.join(DATA_DIR, 'train2017/train2017')
ANN_FILE   = os.path.join(DATA_DIR, 'annotations', 'instances_train2017.json')
OUT_DIR    = 'captcha_grids_random'
LABELS_FILE_TRAIN = os.path.join(OUT_DIR, 'labels_train.csv')
LABELS_FILE_VAL = os.path.join(OUT_DIR, 'labels_val.csv')
LABELS_FILE_TEST = os.path.join(OUT_DIR, 'labels_test.csv')
N_SAMPLES  = 100    # nombre de grilles à générer
GRID_SIZE  = 3      # 3×3
CELL_SIZE  = 128    # taille (px) de chaque vignette


os.makedirs(OUT_DIR, exist_ok=True)

def generate_dataset(out_dir, n_samples, grid_size, cell_size):
  # Charge COCO
  coco = COCO(ANN_FILE)

  # Prépare toutes les catégories ayant au moins une image
  all_cat_ids = coco.getCatIds()
  cat_to_img = {
      cid: coco.getImgIds(catIds=[cid])
      for cid in all_cat_ids
  }
  # Ne garder que celles avec images
  valid_cats = [cid for cid, imgs in cat_to_img.items() if imgs]

  for i in range(N_SAMPLES):
      # Choix aléatoire de la catégorie cible
      cat_id = random.choice(valid_cats)
      cat_info = coco.loadCats(cat_id)[0]
      cat_name = cat_info['name']
      img_ids_pos = cat_to_img[cat_id]
      # Prépare liste négative pour cette catégorie
      img_ids_neg = list(set(coco.getImgIds()) - set(img_ids_pos))

      # Position aléatoire dans la grille
      target_pos = random.randrange(GRID_SIZE**2)

      # Nouvelle image 3×3
      grid_img = Image.new('RGB', (CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE), (255,255,255))
      for idx in range(GRID_SIZE**2):
          if idx == target_pos:
              img_id = random.choice(img_ids_pos)
          else:
              img_id = random.choice(img_ids_neg)

          info = coco.loadImgs(img_id)[0]
          path = os.path.join(IMG_DIR, info['file_name'])
          img = Image.open(path).convert('RGB').resize((CELL_SIZE, CELL_SIZE))
          x, y = (idx % GRID_SIZE) * CELL_SIZE, (idx // GRID_SIZE) * CELL_SIZE
          grid_img.paste(img, (x, y))

      # Annoter label (optionnel)
      draw = ImageDraw.Draw(grid_img)
      font = ImageFont.load_default()
      label_grid = [0 for i in range(GRID_SIZE**2)]
      label_grid[target_pos] = 1
      label = f"pos={target_pos} cat={cat_name}"
      draw.text((5, GRID_SIZE*CELL_SIZE - 12), label, fill=(0,0,0), font=font)

      # Sauvegarde
      out_path = os.path.join(OUT_DIR, f'grid_{i:03d}.jpg')
      grid_img.save(out_path)

      # Aperçu pour les 3 premiers
      if i < 3:
          display(grid_img)
          print(label)

  print("Terminé — grilles dans", OUT_DIR)
