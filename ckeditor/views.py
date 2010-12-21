import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
            
try: 
    from PIL import Image, ImageOps 
except ImportError: 
    import Image, ImageOps

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    # monkey patch this with a dummy decorator which just returns the same function
    # (for compatability with pre-1.1 Djangos)
    def csrf_exempt(fn):
        return fn
        
THUMBNAIL_SIZE = (75, 75)

# Use Django Storage API
from django.core.files.storage import get_storage_class
storage_class = get_storage_class()
storage = storage_class(location=settings.CKEDITOR_UPLOAD_PATH, base_url=settings.CKEDITOR_UPLOAD_URL)
   
def get_available_name(name):
    """
    Returns a filename that's free on the target storage system, and
    available for new content to be written to.
    """
    return storage.get_available_name(name)

def get_thumb_filename(file_name):
    """
    Generate thumb filename by adding _thumb to end of filename before . (if present)
    """
    return '%s_thumb%s' % os.path.splitext(file_name)

def create_thumbnail(filename):
    image = Image.open(storage.open(filename))
        
    # Convert to RGB if necessary
    # Thanks to Limodou on DjangoSnippets.org
    # http://www.djangosnippets.org/snippets/20/
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
       
    # scale and crop to thumbnail
    imagefit = ImageOps.fit(image, THUMBNAIL_SIZE, Image.ANTIALIAS)

    thumb_filename = get_thumb_filename(filename)
    imagefit.save(storage.open(thumb_filename, 'w'))

        
def get_media_url(path):   
    return storage.url(path)


def get_upload_filename(upload_name, user):
    # If CKEDITOR_RESTRICT_BY_USER is True upload file to user specific path.
    if getattr(settings, 'CKEDITOR_RESTRICT_BY_USER', False):
        user_path = user.username
    else:
        user_path = ''

    # Generate date based path to put uploaded file.
    date_path = datetime.now().strftime('%Y%m%d')
    
    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(
            user_path,
            date_path,
            storage.get_valid_name(upload_name)
            )
      
    # Get available name and return.
    return storage.get_available_name(upload_path)
     
    
@csrf_exempt
def upload(request):
    """
    Uploads a file and send back its URL to CKEditor.

    TODO:
        Validate uploads
    """
    # Get the uploaded file from request.
    upload = request.FILES['upload']

    upload_filename = get_upload_filename(upload.name, request.user)

    storage.save(upload_filename, upload)

    create_thumbnail(upload_filename)

    # Respond with Javascript sending ckeditor upload url.
    url = storage.url(upload_filename)

    return HttpResponse("""
    <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction(%s, '%s');
    </script>""" % (request.GET['CKEditorFuncNum'], url))

def get_image_browse_urls(user=None):
    """
    Recursively walks all dirs under upload dir and generates a list of
    thumbnail and full image URL's for each file found.
    """
    images = []
    
    # If a user is provided and CKEDITOR_RESTRICT_BY_USER is True,
    # limit images to user specific path, but not for superusers.
    if user and not user.is_superuser and getattr(settings, 'CKEDITOR_RESTRICT_BY_USER', False):
        user_path = user.username
    else:
        user_path = ''

    browse_path = os.path.join(settings.CKEDITOR_UPLOAD_PATH, user_path)
    
    for root, dirs, files in os.walk(browse_path):
        for filename in [ os.path.join(root, x) for x in files ]:
            filename = filename.replace(settings.CKEDITOR_UPLOAD_PATH,'')
            # bypass for thumbs
            if '_thumb' in filename:
                continue
            
            images.append({
                'thumb': storage.url(get_thumb_filename(filename)),
                'src': storage.url(filename)
            })

    return images
    
def browse(request):
    context = RequestContext(request, {
        'images': get_image_browse_urls(request.user),
        'media_prefix': settings.CKEDITOR_MEDIA_PREFIX,
    })
    return render_to_response('browse.html', context)
