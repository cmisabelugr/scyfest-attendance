import random, string

from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse

def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(6))
    return result_str

# Create your models here.

class Ticket(models.Model):

    name = models.TextField(verbose_name=_("Person name"), blank=True)
    has_tui = models.BooleanField(verbose_name=_("Has TUI?"), blank= False, default=True)
    from_college = models.BooleanField(verbose_name=_("Is from Ysabel?"), default = False)
    checkedin = models.BooleanField(verbose_name=_("Is inside the building?"), default = False)
    active = models.BooleanField(verbose_name=_("This ticket is active?"), default = False)
    qr_text = models.TextField(verbose_name=_("QR Text label"), blank=False, default=get_random_string, unique=True)
    profile_picture = models.ImageField(verbose_name="Profile picture", blank=True)

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def save(self, *args, **kwargs):
        if(self.profile_picture):
            self.profile_picture = make_profile(self.profile_picture)
            #self.foto = make_thumbnail(self.foto, size=(200, 200))

        super().save(*args, **kwargs)

    def __str__(self):
        if self.active:
            if self.name:
                return "Ticket {} activo de {}".format(self.id, self.name)
            else:
                return "Ticket {} activo".format(self.id)
        else:
            return "Ticket {} no activado".format(self.id)

    def get_absolute_url(self):
        return reverse("Ticket_detail", kwargs={"pk": self.pk})

    def get_points(self):
        p = self.points_set.aggregate(Sum('value'))['value__sum']
        if p is None: p = 0
        return p
    
    def get_boothpoints(self):
        p = self.boothpoints_set.aggregate(Sum('value'))['value__sum']
        if p is None: p = 0
        return p


class Points(models.Model):

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name="Numero de puntos")
    activity = models.TextField(verbose_name="Veterano")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "puntos"
        verbose_name_plural = "puntos"

    def __str__(self):
        return (str(self.value) + " points to " + str(self.ticket) + " by " + self.activity) 

    def get_absolute_url(self):
        return reverse("puntos_detail", kwargs={"pk": self.pk})
    
class BoothPoints(models.Model):

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name="Numero de puntos")
    activity = models.TextField(verbose_name="Fotomaton")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "puntos_fotomaton"
        verbose_name_plural = "puntos_fotomaton"

    def __str__(self):
        return (str(self.value) + " photobooth points to " + str(self.ticket) + " by " + self.activity) 

    def get_absolute_url(self):
        return reverse("photopuntos_detail", kwargs={"pk": self.pk})

from io import BytesIO
from django.core.files import File
from PIL import Image, ExifTags
from autocrop import Cropper
from numpy import asarray


def make_thumbnail(image, size=(200, 200)):
    """Makes thumbnails of given size from given image"""

    im = Image.open(image)

    im.convert('RGB') # convert mode

    im.thumbnail(size) # resize image

    thumb_io = BytesIO() # create a BytesIO object

    im.save(thumb_io, 'JPEG') # save image to BytesIO object

    thumbnail = File(thumb_io, name=image.name) # create a django friendly File object

    return thumbnail

def make_profile(image):
    """Makes thumbnails of given size from given image"""
    cropper = Cropper()
    im = Image.open(image)

    im = im.convert('RGB') # convert mode

    for orientation in ExifTags.TAGS.keys() : 
        if ExifTags.TAGS[orientation]=='Orientation' : break 
    try:
        exif=dict(im._getexif().items())

        if   exif[orientation] == 3 : 
            im=im.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6 : 
            im=im.rotate(Image.ROTATE_180)
        elif exif[orientation] == 8 : 
            im=im.rotate(Image.ROTATE_180)
    except:
        pass
    array = asarray(im)
    print("Procesando imagen")
    cropped_array = cropper.crop(array)

    if cropped_array is None:
        print("No se ha encontrado cara")
        cropped_array = array
    else:
        print("Se ha encontrado cara y se ha flipeado")
        cropped_array = cropped_array[:, :, [2, 1, 0]]

    cropped_image = Image.fromarray(cropped_array)

    thumb_io = BytesIO() # create a BytesIO object

    cropped_image.save(thumb_io, 'JPEG') # save image to BytesIO object

    thumbnail = File(thumb_io, name=image.name+'.jpg') # create a django friendly File object

    return thumbnail

class Fotomaton(models.Model):

    picture = models.ImageField(verbose_name="Profile picture", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    view_counter = models.IntegerField(verbose_name="Veces mostrada", )

    class Meta:
        verbose_name = _("Fotomaton")
        verbose_name_plural = _("Fotomatons")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Fotomaton_detail", kwargs={"pk": self.pk})
