from django.shortcuts import render
from .forms import QRCodeForm
import qrcode
from django.conf import settings
import os

def generate_qr_code(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST) # create a form object with data # request.POST is data
        # print(form)
        # print(request.POST)
        # request.POST = <QueryDict: {'csrfmiddlewaretoken': ['LLhHOeqKDcj9fUbpHDNpNnWfZ2KVMIph66uAOepnPwNOy9dyABVFVzMarCKV8j1j'], 'restaurant_name': ['google'], 'url': ['http://google.com']}>
        
        if form.is_valid():
            res_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']
            # print(res_name, url)
            # Generate QR Code
            qr = qrcode.make(url)
            # print(qr) # <qrcode.image.pil.PilImage object at 0x00000292D9E53350>
            # type(qr) , qrcode.image.pil.pilImage
            # qr.save('test_qr.png')# this is static file name # save the qr code into png file(file name is test_qr.png)
            file_name = res_name.replace(" ","_").lower()+'_menu.png' # replce all the place with _ then convert into lower the add _menu.png 
            file_path = os.path.join(settings.MEDIA_ROOT, file_name) # ../media/rathan_rest_menu.png
            # print('file path==>', file_path) # C:\Users\Udit Narayan Nayak\OneDrive\Desktop\qr-code-django\media\google_menu.png
            qr.save(file_path)
            # qr.save(file_name) # dynamic file name

            # Create Image URL
            qr_url = os.path.join(settings.MEDIA_URL, file_name)

            # print('media url==>', qr_url) # /media/google_menu.png

            context = {
                'res_name': res_name, 
                'qr_url': qr_url,
                'file_name': file_name
            }
            return render(request, 'qr_result.html', context)

    else:
        form = QRCodeForm()
        context = {
            'form':form,
        }
        return render(request, 'generate_qr_code.html', context)