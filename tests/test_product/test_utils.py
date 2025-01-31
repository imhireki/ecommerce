from PIL.Image import Resampling
import pytest

from apps.product import utils


@pytest.mark.unit
def test_make_thumbnail(mocker):
    thumbnail_io = mocker.patch("apps.product.utils.BytesIO")()
    content = mocker.patch("apps.product.utils.ContentFile")
    pil_img = mocker.patch("PIL.Image.open").return_value.__enter__.return_value
    resized_img = pil_img.resize.return_value

    size = (640, 360)
    image = mocker.Mock()
    thumb = utils.make_thumbnail(image, size)

    pil_img.resize.assert_called_with(size, Resampling.LANCZOS, reducing_gap=2)
    resized_img.save.assert_called_with(
        thumbnail_io, pil_img.format, optimize=True, quality=85
    )
    content.assert_called_with(thumbnail_io.getvalue(), name=image.name)
    assert thumb == content.return_value
