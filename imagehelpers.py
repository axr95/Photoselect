import tkinter as tk
from os.path import basename

import PIL
from PIL import ImageTk, Image, ImageOps

class ImageControlsGroup(object):
    SIZES = {"MAIN": (600, 600), "SIDE": (400, 400), "THUMBNAIL": (128, 128)}

    def __init__(self, base, image_label, name_checkbox, index_offset, size_name, is_thumbnail=False):
        if not SelectImage.PLACEHOLDER_IMAGE:
            SelectImage.PLACEHOLDER_IMAGE = tk.PhotoImage(data=SelectImage.PLACEHOLDER_IMG_BASE64_GIF)

        self.base = base
        self.lblImage = image_label
        self.chkName = name_checkbox
        self.offset = index_offset
        self.sizeName = size_name
        self.isThumbnail = is_thumbnail

        self._photoImage = None
        self._image = None


    def reload_view(self):
        idx = self.base.cur_idx + self.offset
        size = ImageControlsGroup.SIZES[self.sizeName]
        if 0 <= idx < len(self.base.images):
            if self._image != self.base.images[idx]:
                self._image = self.base.images[idx]
                self.chkName.configure(text=self._image.name, wraplength=size[0],
                                       variable=self._image.selected, state=tk.ACTIVE)

            if self.isThumbnail:
                if self.base.showPreviews.get() == 1:
                    self._photoImage = self.base.images[idx].get_thumbnail()
            else:
                self._photoImage = self.base.images[idx].get_image(size=size)
        else:
            self.chkName.configure(variable=None, state=tk.DISABLED)
            self.chkName.deselect()

            self._photoImage = SelectImage.PLACEHOLDER_IMAGE
            self._image = None
            if idx == -1:
                self.chkName.configure(text="[Anfang]")
            elif idx == len(self.base.images):
                self.chkName.configure(text="[Ende]")
            else:
                self.chkName.configure(text="")

        self.lblImage.configure(image=self._photoImage, width=size[0], height=size[1])


class SelectImage(object):
    PLACEHOLDER_IMG_BASE64_PNG = "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"
    PLACEHOLDER_IMG_BASE64_GIF = "R0lGODlhgACAAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAACH5BAEAAPwALAAAAACAAIAAAAj/AIkpE0hwoMGCCA8qTMhwocOGEB9KjEhxosOBnwx+ErhRmbJMHkFiHMmxZMiTJDOa7PgRJTGVKpV1ZClS5EuSMk223HmzZ86fO22qFIgxYceCNg2CJCpwqcGWCGMSZDm1YFGFR5V6RPq0qUKoB6VeDWvVKdipC6leZZrVJFeFZr2WTZuW6dqtbX++5Wp3adWnIJ3eFLxRamG2Lwse1po18NaWZh2jJewzMdXFJRvrhfy4a1bAXTfrRNs39OfKOLV6toqap2rEnQW71EhM7smlahOvxpowqW2tc6PWfawbtuLexMECB21Xt0PcsIFrDntXdseksnFT55v1M/TlVzUn/5zt/DTPxcRjgsyrN2PcseiPF8341Slmj2Md01X9PrLxi7r5BtdJrEnXHHPs/ZWXfO9xR1Zy3/mU3081TQTTgX8J+KBsvJ1VH04MXRdaVF5p+FdDDs1kGWsiFkYXMWjEKOMkMdKIxnzF4YVjbiq699RVjuWWHo78EXhYgkZWVCMaNtI4yZNMRtlklEmGZmBypJn4IYaPLWhliQCeRJMyM0pppplOokllVeYh1iZePlXo1JwpkbbYd6GtFyBcaULZp5p/BholGnZxVuFcenooW4EjhtkonRYNpCaglAoqqG1MsRVpodrtuWeFUIkIKmr2lbSkpUyKcRBCBFV65oj0Uf/W3o4FFlprmBG5OJqrNBZ4qFi1KSMGqr36GKxXL9qa052myWXss3V62Sqqx4ZKkYpbubqdYW55JCKKyHJ4K7i0UXiqmcF5ltJDbVF6o1EHLmUdUaMOpKmn0K6IbUFMCtphnez2JJZNZ0JJ4YBJdXnig3dx+RWGMFm6cI70WosleQad2QiTZKklr0TfhhQiZ6FyFu5Bgr57lLEANwvwp5I6meaNaoXZIougucZluhWf2+uXzA3YU7eMJjQsmhkGddeGuIL1Xae7XQqnyZeNBqLSzCqnJrCdwfbea7qOpaynkiI99dg6e+gcucahOYnAAzn2Nb4TA7VnyGEFGuGFJaf/m6hJf39L1aSEPozg2l0rLDSAYat5oOEd36p2ubAKBCiNVFsk2b7SqbunQo4XSTePJ5emqMlkpvzzcNg2WjHE40LlM9G7NRfT1fqRCLSZjQj757oNQceynci+zrdAfxYHE+pgtSXeY3gKPNWUk3SU/EV6Clkx9sshvtG5aI873XjiEjhg6B/9fujDnL8l2Wa+WY8u00Jltt26hBEJt+XXH3U9m2KLXHJgtTgYoaklbeKaW6QlGovAiEYbextW1JS2pOXJWX+5X0fQVDPd5CVCefrJylZCwk+oz3wPnJ9t+jOWys3nImbD4IA6eCEFuu5iB0QO/6TkmqpZqX52S49c/9AEQvkILYEns5jgUpim8DTnTMW7S8iC5yHP/O44xxNRCHO0Ke8o40+Fi9dBzMSwbs1rWasR1RdV2MCdkUw40uuR7gIFpNSA5HfDiWIFIYcQFXYHcChZ1PLG4zDfLIlJsSNMnzy4F7GN7m47pJIPdeiyEIFpRe2x3Py+gx6CzQyO0Jsa0BoVsyhVSyhKo1W5wuaoAvXLlAO81VLImKMiVgcnETqXjiryuEU9CFtPS92p+sasHOHRahUbUx51tEjblW5ly9HP+3gpzDRFBHKztKbTlMaqg53mKLTU4uMWCLS5pLJCG7kibbIGQlo2TXKT6QoU6yK4gG3TgQ6p0dG80v9BkE1rTYNEZy0bdhV3InCcnYPXbV6oHceoMyICVc8aneTLi2FsTK2SEuJOFj3g8fGjs5No9vBpwCZKj5HsKmM137UWL23xOUpkU7AoSJqLOes17kRLHscXqkUaZpUYHJM4SRkXE5rNeQoS4xib5CnL7AaXC3GngAiZOPJN7T4oSxXmsrNLIdptg00s5xurKLD/OZFqMOMmQTNzE/C9hp5cEsw868WqD0ZVm1EsGknPcryshrU0n+NKyDy5phRJKJl2mijHsHNQYgKsXuxTSujKN6BWtsSnFjsO7aI6qNeR8po7K+ZlzerUwUyooWLL6VVrVUOT9KlDjNRiMKVZVeL/uFV7X0IbcAb1tqFmsKJ9tCZmbKgcxDFNemSaX2U3VzqLJUW57kscMIsC3S321WPdk0jqTIo6WcIWS2Clki39ol2isBFvLNLdhLCWGN6qzC7TdY1yOMmUT37Ji3QrJeY2Ol3P5rVpoasbFfnyqGpOwlpq+WajquscXwpWoXLK2ENvR8LGlguLxZlZOSn8R13x1mIzRCaccOsVszFWVggDzUZ8tck6NlIibNRKg174GwD6hHfP28sUsxs0BoeQSEAMZ41lW1kZ5vO13VImIWMiHrHoV2XcPIp3//kzeH70vzIWZgRvNOMmt/R+V2KjEb3WtYy8NlFyWygmpxO9AHf3/62xuxLoTDrF63Aol51NXNOKDGPSxgZE8RWeJVVS3QDipzX8Mune6phZGvPNvWLKYOysmjOGfDh6RJZhNmH5XTfu0SkPfSuao/xmOmErxhSzVyw7E86WxvFlfNMI+PSY6l6m1I1MfG/ORDI1QfsOllamJPceOImjHfjEh5NjZHX3HTEnaKNWIiN9SRY/lDrFvRIMYI0Zd7p+PtlqTxPOqHM96RdZlCBXfB5++VZtbpXsjkvq2GffROX36orJKxwJJ91a07W96Z033OHqSHQhXuf7svEObbmf6KcwbqYr1W4saven7FyfFUCVAVaLL07b8+jGvf7FamkZt3CFiZnRJ/9yN7y5O2OIzpmMngNNg9gNIX1XiRjH9NGPh2NFjR5OaesbiePIVuu+FXhynFppbQbmSJsD9tfFmpzhjHM9mNoPNUm7c5IwA/Nr+VdkEtUwFl18b6bwe5A2LRdkaecwgRdupKRK76Hlyd2R4Zrf9lziDWX1qwWGWneTLApy54ctL5f1gAIN4g+JWdM9b/pnpVL8XOitWuRI5E+NILFzl6ZX4pVdwsBu44TkfihppyaelvFZlpHbeTWumapGse8RV+hMFIJ+4DtSdVdOGOc4Ypm1MkSpsW9EYz1HxzZqmadLvxXDWRHdcKMG8YFyg7SIi1amIXy8w3WSiYSkWz7KauyifUB7swf5uCJpQ/pKq7fAioFkdmcz1Fp3sxj03s/tx7a5Y5Xn2USBs+43RFM+pDmutmq1pxnpJCUM1HbgQUWvgkmGtEiTg0oWdi+M5yMaIhtu5X+mZVpghlKHpVodkzyawVgQMTxp5yDd5xKohk8Rp1DFISXD4lvrZ04LQ1tnFH0tN3dN8X1nVUSYcjAQcUwF9SetgzMIhXFO1ikq8R3qpG3S/5V0xaVzIvEJk5UtfjZyKRdULRSEbJNcPoUoKOdiy7QQOPcqGEE9YdRXmCRizpQj9QdIPcFBuqNXZqF2ZXZTZYNXNXgxNcNXJCQhDegh7SKBHRhIIAZEZEZIS6E+vDdUIMRACnNY8hV54MMeDkaA/KVWtwcodmh1kbYsS+crp2Np6iQkRDZ+FGZ0S3aGqLJEfxRE1yRn4HdqWfhm3KNScHQk9EItn9VAm+NiLcc5nIVkrRVKNHh/hQd7fuVH/OSF/5Yw+CIRFeI45jF1jAFtdgVIZ4UGW7ZfKYh2mydpQVNxT1ZlaDVcbPcJgwVVT/dyCphYWPdwpgNJBXQSFCRWlf/GZ7/4dO5XhGEYMM4jfdioM2IxdCyzPg7CFzcFgbyBJAa0ZTHyS0lHVaDCXKIGhsp1f/I2feX2IVPYMG7DZeDVIbY0ZWsxKQQhSFe3ehjVIzEFikYERpDnak7meQ05Gz7DMT8SdMxISuW1LZOnO5UScPWkV91jVA3nJMRgSzHVX99CNhMXc6jXjDODBkwoVnIYHyslg8VFhmJEikDjJeKUai52OaHnkG14MZmwk9xFkEDmVUUldxVmeS1jK8QSI/mDNolSI6jSSvZHjjw2lyHGE6mGkdrXJ1DCMZckisL0Sp5IdkF4cRzVa0bWb0MCXwVyGqozKJOSl/+TYJTmYDb/FH42diXYZzyLyCug6So3uGuGdR84SBLcCEofmF3btlSfyStooipLdmEmuXgMiFBQkztOhG/JkTWJxpsSs1rUeDXlpUxPo3dhMk0CSVZOp5uoQigWxGzmc1wu8j6UxZeNppnlORy+5GAEsZ49SU+nt071uGouGSf6l3QKGYXOpzhFdZxo1BQwOHtIhV38J1/MyB1ckmn4BZeZyJ6SxjJq1XmhJHdHZGgdpWo7Vj5zA5Y1hBNedI91eSRSFEUdVXuAFTYWyFbwA4WAZlhXc1jt857gtzjz+RH3Qm/3EY2JM263VGt1ZmtqA03yoWDwpGCoVTt615iWZHzAaTuiA5KoXoSZKIp6WeSFMgk06elRmzdfRmIhUaqJsklQ+giCXkSdFfacbgRcErd3joZoShpMDckj8ImN26ZGBmk/QMSLy3aEBqhWwdSPyzQ25Rd45PkgBfpzVDSO4FU0ICoQAQEAOw=="

    PLACEHOLDER_IMAGE = None  # can not create PhotoImage at this point

    THUMBNAIL_SIZE = 64, 64

    def __init__(self, path):
        if not SelectImage.PLACEHOLDER_IMAGE:
            SelectImage.PLACEHOLDER_IMAGE = tk.PhotoImage(data=SelectImage.PLACEHOLDER_IMG_BASE64_GIF)

        self.name = basename(path)
        self.path = path
        self.thumbnail = None
        self.selected = tk.BooleanVar()

        self.prepared = None
        self.preparedSize = None

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail

        self.thumbnail = self.get_image(SelectImage.THUMBNAIL_SIZE)
        # print("thumbnail created for", self.name)
        return self.thumbnail

    def get_image(self, size=None):
        if size and self.prepared and self.preparedSize == size:
            return self.prepared
        try:
            with Image.open(self.path) as im:
                if size:
                    #im.draft('RGB', size)
                    im.thumbnail(size)
                res = ImageTk.PhotoImage(ImageOps.exif_transpose(im))
                # print("image_get for", self.name)
                self.prepared = res
                self.preparedSize = size
        except PIL.UnidentifiedImageError:
            res = SelectImage.PLACEHOLDER_IMAGE

        return res

    def __str__(self):
        return self.name
