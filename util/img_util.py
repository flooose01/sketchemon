import base64
from io import BytesIO
from PIL import Image

def b64_to_pil(b64: str):
  return Image.open(BytesIO(base64.b64decode(b64)))

def pil_to_b64(pil: Image):
  im_file = BytesIO()
  pil.save(im_file, format="png")
  im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
  return base64.b64encode(im_bytes)