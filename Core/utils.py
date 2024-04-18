from jdatetime import datetime as jdatetime_dt

def get_upload_path(model_name, file_name, file_ext):
    return '{}/{}.{}'.format(model_name, file_name, file_ext)

def change_image_name(image_field,model_name,title):
    old_file_name , file_ext = image_field.name.rsplit('.',1)
    return get_upload_path(model_name, title, file_ext)