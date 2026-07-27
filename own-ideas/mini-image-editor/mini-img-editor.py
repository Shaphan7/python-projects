from argparse import ArgumentParser
from pathlib import Path
parser = ArgumentParser()
import numpy as np
from PIL import Image

parser.add_argument("img_path")
parser.add_argument("action")
parser.add_argument("--amount", default="100")
parser.add_argument("--newname", default=None)
parser.add_argument("--stats", action="store_true")
args = parser.parse_args()
path = Path(args.img_path)
def invert(array):
    return 255 - array

def brighten(array, amount):
    array = array.astype(np.int32)
    return np.clip(array + amount, 0, 255).astype(np.uint8)

def print_stats(array):
    print(f"Shape: {array.shape}\n" \
      f"Dtype: {array.dtype}\n" \
      f"Min: {array.min()}\n" \
      f"Max: {array.max()}\n" \
      f"Mean(Average): {array.mean()}")

def save(img_array, action):
    result_img = Image.fromarray(img_array)
    if action == "grey":
        result_img = result_img.convert("L")
        img_array = np.array(result_img)
    if args.newname is None:
        # I know very specific
        result_img.save(f"./{action}ed-{path.name}")
    else:
        result_img.save(f"./{args.newname}.jpg")
    print("Image has been edited and saved!")
    if args.stats:
        print_stats(img_array)

def handle_action():
    img = Image.open(args.img_path)
    img_array = np.array(img)
    if args.action == "invert":
        result_array = invert(img_array)
        save(result_array, "invert")
    elif args.action == "brighten":
        result_array = brighten(img_array, int(args.amount))
        save(result_array, "brighten")
    elif args.action == "grey":
        save(img_array, "grey")
    else:
         return print(f"'{args.action}' is an invalid action!")

def main():
    if not path.exists():
        return print("Invalid image path!")
    if not path.name.endswith((".jpg", ".png")):
        return print("Invalid image format!")
    if not args.amount.isdigit():
        print(args.amount)
        return print("Amount must be a number!")
    handle_action()

main()
