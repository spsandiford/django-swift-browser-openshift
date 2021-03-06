from django import forms

class ContainerNameField(forms.CharField):
    """
    From the Spec, Container names can be up to 256 bytes
    in length and cannot contain '/' character
    see: https://docs.openstack.org/swift/latest/api/object_api_v1_overview.html
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 256
        super().__init__(**kwargs)

    def to_python(self, value):
        return super().to_python(value)

    def validate(self, value):
        super().validate(value)
        if '/' in value:
            raise ValidationError('Container names cannot contain slash(/) character')


class ObjectNameField(forms.CharField):
    """
    From the Spec, Object names can be up to 1024 bytes
    by default there are no character restrictions
    see: https://docs.openstack.org/swift/latest/api/object_api_v1_overview.html
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1024
        super().__init__(**kwargs)

    def to_python(self, value):
        return super().to_python(value)

    def validate(self, value):
        super().validate(value)


class CreateContainerForm(forms.Form):
    """ Simple form for container creation """
    container = ContainerNameField(label='Container Name')

class DeleteContainerForm(forms.Form):
    """ Simple form for container delete """
    container = ContainerNameField(label='Container Name')

class UploadFileForm(forms.Form):
    """ Form to allow uploading a file to be pushed to a container """
    file = forms.FileField()
    container = ContainerNameField(label='Container')
    subdir = ObjectNameField(label='Subdirectory', required=False)
    object_name = ObjectNameField(label='Object Name')

class CreateFolderForm(forms.Form):
    container = ContainerNameField(label='Container Name')
    subdir = ObjectNameField(label='Subdirectory', required=False)
    folder_name = forms.CharField(label='Folder Name', max_length=256)

