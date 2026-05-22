import os
import mimetypes
import re
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render


def index(request):
    # claude修改: 登录页面视图
    return render(request, 'login.html')


def main(request):
    # claude修改: 数据看板页面视图
    return render(request, 'main.html')


def serve_processed(request, path):
    # claude修改: 处理后视频文件服务视图，支持Range请求以实现视频拖拽播放
    file_path = Path(settings.PROCESSED_DIR) / path
    file_path = file_path.resolve()
    processed_root = Path(settings.PROCESSED_DIR).resolve()
    if not str(file_path).startswith(str(processed_root)):
        raise Http404("File not found")
    if not file_path.exists() or not file_path.is_file():
        raise Http404("File not found")

    file_size = file_path.stat().st_size
    content_type = 'video/mp4'
    content_type_guess, _ = mimetypes.guess_type(str(file_path))
    if content_type_guess:
        content_type = content_type_guess

    # claude修改: 手动处理HTTP Range请求，Django dev server的FileResponse对Range支持有限
    range_header = request.headers.get('Range', '')
    if range_header:
        m = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else file_size - 1
            end = min(end, file_size - 1)
            length = end - start + 1
            with open(file_path, 'rb') as f:
                f.seek(start)
                data = f.read(length)
            response = HttpResponse(data, status=206, content_type=content_type)
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            response['Content-Length'] = str(length)
            response['Accept-Ranges'] = 'bytes'
            response['Content-Disposition'] = 'inline'
            return response

    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Length'] = file_size
    response['Content-Disposition'] = 'inline'
    response['Accept-Ranges'] = 'bytes'
    return response
