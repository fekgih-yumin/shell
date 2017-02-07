# coding=utf-8
# 用于上传文件到oss
import oss2
import time


AccessKeyId='pK9W8QO71s1w18N9'
AccessKeySecret='BdbAXcq1pnE4xZaBNryBR8MMkuGEy0'
Endpoint='oss-cn-shenzhen.aliyuncs.com'
bucket_name= 'wufan-picture-app'
bucket_name_customer= 'pictures-customer'
# bucket_name2= 'pictures-raw'
def push_image(path, first_type,seconde_type,format,i):
    # t=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    try:
        auth=oss2.Auth(AccessKeyId,AccessKeySecret) #oss2.Auth承载用户的验证信息
        # service = oss2.Service(auth,Endpoint)   #oss2.Service对象用于服务相关的操作，目前是用来列举Bucket
    except:
        print "添加用户信息和操作失败"
    # try:
    #     print ([b.name for b in oss2.BucketIterator(service)])  #oss2.Bucketlterator对象是一个可以遍历用户Bucket信息的迭代器
    # except:
    #     print "遍历Bucket失败"
    try:
        oss_path='%s/%s/%s_%s_%s.%s' %(first_type,seconde_type,first_type,seconde_type,i,format)
        bucket=oss2.Bucket(auth, Endpoint, bucket_name)
        print oss_path
        bucket.put_object_from_file(oss_path,path)
    except:
        print "上传失败"
    return oss_path

def push_image_customer(path, type):
    t=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    try:
        auth=oss2.Auth(AccessKeyId,AccessKeySecret) #oss2.Auth承载用户的验证信息
        # service = oss2.Service(auth,Endpoint)   #oss2.Service对象用于服务相关的操作，目前是用来列举Bucket
    except:
        print "添加用户信息和操作失败"
    # try:
    #     print ([b.name for b in oss2.BucketIterator(service)])  #oss2.Bucketlterator对象是一个可以遍历用户Bucket信息的迭代器
    # except:
    #     print "遍历Bucket失败"
    try:
        oss_path='customer/%s/%s_%s.jpg' %(type,t,type)
        bucket=oss2.Bucket(auth, Endpoint, bucket_name)
        print oss_path
        bucket.put_object_from_file(oss_path,path)
    except:
        print "上传失败"
    return oss_path
