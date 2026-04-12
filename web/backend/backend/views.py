from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.static import serve as static_serve


def index(request):
    return render(request, 'login.html')#改过  以前是main  现在是进入登陆页面！

def main(request):
    # 这个返回大盘  main.html
    return render(request, "main.html")

def serve_processed(request, path):
    # 仅用于演示环境，生产建议由Nginx等直接静态托管
    root = Path(settings.PROCESSED_DIR)
    return static_serve(request, path, document_root=str(root))