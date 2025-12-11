# coding=utf-8
import os
import logging
from pathlib import Path

# 配置你的云存储信息
# 从环境变量读取配置
CLOUD_CONFIG = {
    "enabled": os.environ.get("CLOUD_SYNC_ENABLED", "false").lower() == "true",
    "provider": os.environ.get("CLOUD_PROVIDER", "aliyun"),  # aliyun, aws, tencent, etc.
    "access_key": os.environ.get("CLOUD_ACCESS_KEY", ""),
    "secret_key": os.environ.get("CLOUD_SECRET_KEY", ""),
    "bucket_name": os.environ.get("CLOUD_BUCKET_NAME", ""),
    "region": os.environ.get("CLOUD_REGION", ""),
    "endpoint": os.environ.get("CLOUD_ENDPOINT", ""),  # optional
}

def upload_to_cloud(local_file_path: str, remote_file_name: str = None) -> str:
    """
    上传文件到云存储
    
    Args:
        local_file_path: 本地文件绝对路径
        remote_file_name: 云端保存的文件名（包含路径），如果为None则使用本地文件名
        
    Returns:
        str: 上传后的公开访问URL（如果支持），或者上传状态消息
    """
    if not CLOUD_CONFIG["enabled"]:
        return "Cloud sync disabled"

    if not os.path.exists(local_file_path):
        return f"File not found: {local_file_path}"

    if remote_file_name is None:
        remote_file_name = Path(local_file_path).name

    try:
        if CLOUD_CONFIG["provider"] == "aliyun":
            return _upload_to_aliyun_oss(local_file_path, remote_file_name)
        elif CLOUD_CONFIG["provider"] == "aws":
            return _upload_to_aws_s3(local_file_path, remote_file_name)
        # Add more providers here
        else:
            return f"Unsupported provider: {CLOUD_CONFIG['provider']}"
    except Exception as e:
        print(f"Upload failed: {e}")
        return f"Upload failed: {e}"

def _upload_to_aliyun_oss(local_path, remote_name):
    try:
        import oss2
    except ImportError:
        print("Please install oss2: pip install oss2")
        return "Please install oss2"
    
    try:
        # 使用 AccessKeyId 和 AccessKeySecret 初始化
        auth = oss2.Auth(CLOUD_CONFIG['access_key'], CLOUD_CONFIG['secret_key'])
        # 初始化 Bucket
        # endpoint 示例: http://oss-cn-hangzhou.aliyuncs.com
        endpoint = CLOUD_CONFIG['endpoint']
        if not endpoint.startswith('http'):
            endpoint = 'http://' + endpoint
            
        bucket = oss2.Bucket(auth, endpoint, CLOUD_CONFIG['bucket_name'])
        
        # 上传文件
        print(f"正在上传 {local_path} 到 OSS: {remote_name} ...")
        bucket.put_object_from_file(remote_name, local_path)
        
        # 构造访问 URL (假设 Bucket 权限为公共读)
        # URL 格式: https://bucket-name.endpoint/remote_name
        # 移除 endpoint 中的 http:// 或 https://
        clean_endpoint = endpoint.replace('http://', '').replace('https://', '')
        url = f"https://{CLOUD_CONFIG['bucket_name']}.{clean_endpoint}/{remote_name}"
        
        print(f"上传成功: {url}")
        return url
    except Exception as e:
        error_msg = f"Aliyun OSS upload failed: {str(e)}"
        print(error_msg)
        raise e

def _upload_to_aws_s3(local_path, remote_name):
    # try:
    #     import boto3
    # except ImportError:
    #     return "Please install boto3: pip install boto3"
    
    # s3 = boto3.client('s3', aws_access_key_id=..., ...)
    # s3.upload_file(local_path, CLOUD_CONFIG['bucket_name'], remote_name)
    print("AWS S3 upload implemented (placeholder)")
    return "AWS S3 upload placeholder"
