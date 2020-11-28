import flask
import qrcode
import qrcode.image.svg
import io

def generate(data):
    image = qrcode.make(
        data,
        box_size=50,
        image_factory=qrcode.image.svg.SvgPathFillImage,
    )
    buffer = io.BytesIO()
    image.save(buffer)
    buffer.seek(0)
    return buffer.read()
