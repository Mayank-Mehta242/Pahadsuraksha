import os
import uuid

from werkzeug.utils import secure_filename
from flask import url_for

from config import Config


# =====================================================
# Upload Service
# =====================================================

class UploadService:

    def __init__(self):

        self.upload_folder = Config.UPLOAD_FOLDER

        self.allowed_extensions = {

            "png",
            "jpg",
            "jpeg",
            "gif",
            "webp",
            "pdf"

        }

        self.max_size = 10 * 1024 * 1024      # 10 MB

        self.create_upload_folder()


    # =================================================
    # Create Upload Folder
    # =================================================

    def create_upload_folder(self):

        if not os.path.exists(

            self.upload_folder

        ):

            os.makedirs(

                self.upload_folder

            )


    # =================================================
    # Check Allowed Extension
    # =================================================

    def allowed_file(

        self,

        filename

    ):

        if "." not in filename:

            return False

        extension = filename.rsplit(

            ".",

            1

        )[1].lower()

        return extension in self.allowed_extensions


    # =================================================
    # Validate File
    # =================================================

    def validate_file(

        self,

        file

    ):

        if file is None:

            return {

                "success": False,

                "message": "No file selected."

            }

        if file.filename == "":

            return {

                "success": False,

                "message": "Filename cannot be empty."

            }

        if not self.allowed_file(

            file.filename

        ):

            return {

                "success": False,

                "message": "Unsupported file format."

            }

        return {

            "success": True

        }


    # =================================================
    # Check File Size
    # =================================================

    def validate_size(

        self,

        file

    ):

        file.seek(

            0,

            os.SEEK_END

        )

        size = file.tell()

        file.seek(0)

        if size > self.max_size:

            return {

                "success": False,

                "message": "File exceeds 10 MB limit."

            }

        return {

            "success": True

        }


    # =================================================
    # Generate Secure Filename
    # =================================================

    def generate_filename(

        self,

        filename

    ):

        extension = filename.rsplit(

            ".",

            1

        )[1].lower()

        unique_name = (

            str(uuid.uuid4())

            + "."

            + extension

        )

        return secure_filename(

            unique_name

        )
    # =================================================
    # Save File
    # =================================================

    def save_file(

        self,

        file

    ):

        # Validate File

        validation = self.validate_file(

            file

        )

        if not validation["success"]:

            return validation

        # Validate Size

        size_check = self.validate_size(

            file

        )

        if not size_check["success"]:

            return size_check

        # Generate Secure Filename

        filename = self.generate_filename(

            file.filename

        )

        filepath = os.path.join(

            self.upload_folder,

            filename

        )

        # Save File

        file.save(

            filepath

        )

        return {

            "success": True,

            "filename": filename,

            "filepath": filepath

        }


    # =================================================
    # Upload Image
    # =================================================

    def upload_image(

        self,

        image

    ):

        result = self.save_file(

            image

        )

        if not result["success"]:

            return result

        return {

            "success": True,

            "message": "Image uploaded successfully.",

            "filename": result["filename"],

            "url": self.get_file_url(

                result["filename"]

            )

        }


    # =================================================
    # Upload Document
    # =================================================

    def upload_document(

        self,

        document

    ):

        result = self.save_file(

            document

        )

        if not result["success"]:

            return result

        return {

            "success": True,

            "message": "Document uploaded successfully.",

            "filename": result["filename"],

            "url": self.get_file_url(

                result["filename"]

            )

        }


    # =================================================
    # Generate File URL
    # =================================================

    def get_file_url(

        self,

        filename

    ):

        return url_for(

            "static",

            filename=f"uploads/{filename}",

            _external=True

        )


    # =================================================
    # Upload Incident Image
    #
    # Used by Incident Reporting API
    # =================================================

    def upload_incident_image(

        self,

        image

    ):

        upload = self.upload_image(

            image

        )

        if not upload["success"]:

            return upload

        return {

            "success": True,

            "message": "Incident image uploaded successfully.",

            "image": {

                "filename":

                    upload["filename"],

                "url":

                    upload["url"]

            }

        }
    # =================================================
    # Delete File
    # =================================================

    def delete_file(

        self,

        filename

    ):

        filepath = os.path.join(

            self.upload_folder,

            filename

        )

        if not os.path.exists(filepath):

            return {

                "success": False,

                "message": "File not found."

            }

        os.remove(filepath)

        return {

            "success": True,

            "message": "File deleted successfully."

        }


    # =================================================
    # Get File Information
    # =================================================

    def file_info(

        self,

        filename

    ):

        filepath = os.path.join(

            self.upload_folder,

            filename

        )

        if not os.path.exists(filepath):

            return None

        return {

            "filename": filename,

            "size": os.path.getsize(filepath),

            "path": filepath,

            "url": self.get_file_url(

                filename

            )

        }


    # =================================================
    # List Uploaded Files
    # =================================================

    def list_files(self):

        files = []

        if not os.path.exists(

            self.upload_folder

        ):

            return files

        for filename in os.listdir(

            self.upload_folder

        ):

            filepath = os.path.join(

                self.upload_folder,

                filename

            )

            if os.path.isfile(filepath):

                files.append({

                    "filename": filename,

                    "size": os.path.getsize(filepath),

                    "url": self.get_file_url(

                        filename

                    )

                })

        return files


    # =================================================
    # Total Upload Statistics
    # =================================================

    def upload_statistics(self):

        files = self.list_files()

        total_size = 0

        for file in files:

            total_size += file["size"]

        return {

            "total_files": len(files),

            "total_size": total_size

        }


    # =================================================
    # Clear Upload Folder
    #
    # Admin Only
    # =================================================

    def clear_uploads(self):

        if not os.path.exists(

            self.upload_folder

        ):

            return {

                "success": True,

                "message": "Upload folder already empty."

            }

        deleted = 0

        for filename in os.listdir(

            self.upload_folder

        ):

            filepath = os.path.join(

                self.upload_folder,

                filename

            )

            if os.path.isfile(filepath):

                os.remove(filepath)

                deleted += 1

        return {

            "success": True,

            "message": f"{deleted} files deleted.",

            "deleted_files": deleted

        }
# =====================================================
# Health Check
# =====================================================

    def health_check(self):

        if not os.path.exists(self.upload_folder):

            return {

                "service": "Upload Service",

                "status": "Upload folder missing"

            }

        return {

            "service": "Upload Service",

            "status": "Running",

            "upload_folder": self.upload_folder,

            "allowed_extensions": list(self.allowed_extensions),

            "max_file_size": self.max_size

        }


    # =================================================
    # Check File Exists
    # =================================================

    def file_exists(self, filename):

        filepath = os.path.join(

            self.upload_folder,

            filename

        )

        return os.path.exists(filepath)


    # =================================================
    # Rename Uploaded File
    # =================================================

    def rename_file(

        self,

        old_filename,

        new_filename

    ):

        old_path = os.path.join(

            self.upload_folder,

            old_filename

        )

        if not os.path.exists(old_path):

            return {

                "success": False,

                "message": "File not found."

            }

        extension = old_filename.rsplit(

            ".",

            1

        )[1]

        new_name = secure_filename(

            new_filename

        ) + "." + extension

        new_path = os.path.join(

            self.upload_folder,

            new_name

        )

        os.rename(

            old_path,

            new_path

        )

        return {

            "success": True,

            "filename": new_name,

            "url": self.get_file_url(

                new_name

            )

        }


# =====================================================
# Singleton Instance
# =====================================================

upload_service = UploadService()


# =====================================================
# Utility Functions
# =====================================================

def upload_image(image):

    return upload_service.upload_image(

        image

    )


def upload_document(document):

    return upload_service.upload_document(

        document

    )


def upload_incident_image(image):

    return upload_service.upload_incident_image(

        image

    )


def delete_file(filename):

    return upload_service.delete_file(

        filename

    )


def list_uploaded_files():

    return upload_service.list_files()


def file_information(filename):

    return upload_service.file_info(

        filename

    )


def upload_statistics():

    return upload_service.upload_statistics()


def clear_upload_folder():

    return upload_service.clear_uploads()


def upload_health():

    return upload_service.health_check()


def file_exists(filename):

    return upload_service.file_exists(

        filename

    )