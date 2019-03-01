#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io
import logging
import time
import httplib2

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from oauth2client.contrib.appengine import AppAssertionCredentials

from settings import APPENGINE_SERVICE_ACCOUNT


SCOPES = ['https://www.googleapis.com/auth/drive']


class Drive():
    def __init__(self):
        urlfetch.set_default_fetch_deadline(60)
        self.service = self.get_service()


    def get_service(self):
        # Authorise access to Drive using the user's credentials
        credentials = AppAssertionCredentials(scope=SCOPES)
        http = credentials.authorize(httplib2.Http(memcache))
        # The service object is the gateway to your API functions
        return discovery.build('drive', 'v3', http=http)


    def copy_file(self, source_file_id, file_name, parent_folder_id=None):
        body = {
            "name": file_name
        }
        if parent_folder_id:
            body["parents"] = [parent_folder_id]
        try:
            return self.service.files().copy(fileId=source_file_id, body=body).execute()
        except:
            time.sleep(2)
            try:
                return self.service.files().copy(fileId=source_file_id, body=body).execute()
            except:
                time.sleep(4)
                try:
                    return self.service.files().copy(fileId=source_file_id, body=body).execute()
                except:
                    logging.exception('Tried to copy file in Google Drive. Tried 3 times. Still failed')
                    raise


    def move_file(self, file_id, folder_id, previous_folder=None):
        # Retrieve the existing parents to remove
        if previous_folder:
            previous_parents = previous_folder
        else:
            file = self.service.files().get(fileId=file_id,
                                            fields='parents').execute()

            previous_parents = ",".join(file.get('parents'))

        # Move the file to the new folder
        return self.service.files().update(fileId=file_id,
                                            addParents=folder_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()


    def rename_file(self, file_id, file_name):
        body = {
            "name": file_name
        }

        try:
            return self.service.files().update(fileId=file_id, body=body).execute()
        except:
            time.sleep(2)
            try:
                return self.service.files().update(fileId=file_id, body=body).execute()
            except:
                time.sleep(4)
                try:
                    return self.service.files().update(fileId=file_id, body=body).execute()
                except:
                    logging.exception('Tried to rename file in Google Drive. Tried 3 times. Still failed')
                    raise


    def create_file(self, file, file_name, file_mimetype, drive_mimetype, parents=None):
        body = {
            "name": file_name,
            "mimeType": drive_mimetype
        }

        if parents:
            body['parents'] = parents

        media = MediaIoBaseUpload(file, file_mimetype)  # https://stackoverflow.com/a/11335342

        try:
            return self.service.files().create(
                    body=body, media_body=media
            ).execute()
        except:
            logging.exception('error with create_file. retrying')
            try:
                time.sleep(5)
                return self.service.files().create(
                    body=body, media_body=media
                ).execute()
            except:
                logging.exception('error with create_file. retrying 3rd time')
                try:
                    time.sleep(10)
                    return self.service.files().create(
                        body=body, media_body=media
                    ).execute()
                except:
                    logging.exception('Tried to upload file to Google Drive. Tried 3 times. Still failed')
                    raise


    def transfer_ownership(self, file_id, email, note=None):
        if not email.strip():
            raise Exception('error with email provided. should not be empty')

        body = {
            'role': 'owner',
            'emailAddress': email,
            'type': 'user'
        }
        try:
            if note:
                self.service.permissions().create(fileId=file_id, emailMessage=note,
                                                         transferOwnership=True, body=body).execute()
            else:
                self.service.permissions().create(fileId=file_id, transferOwnership=True,
                                                         body=body).execute()
        except Exception, e:
            logging.exception('error. retrying...')
            try:
                # retry
                time.sleep(10)  # add 10 seconds to avoid errors: https://stackoverflow.com/a/42775241
                if note:
                    self.service.permissions().create(fileId=file_id, emailMessage=note,
                                                             transferOwnership=True, body=body).execute()
                else:
                    self.service.permissions().create(fileId=file_id, transferOwnership=True,
                                                             body=body).execute()
            except:
                logging.exception('error in retry')
                raise Exception('error')



    def make_writeable_to_anyone_with_the_link(self, file_id):
        body = {
            'role': 'writer',
            'allowFileDiscovery': False,
            'type': 'anyone'
        }
        try:
            return self.service.permissions().create(fileId=file_id, body=body).execute()
        except:
            time.sleep(2)
            try:
                return self.service.permissions().create(fileId=file_id, body=body).execute()
            except:
                time.sleep(4)
                try:
                    return self.service.permissions().create(fileId=file_id, body=body).execute()
                except:
                    logging.exception('Tried to make_writeable_to_anyone_with_the_link in Google Drive. Tried 3 times. Still failed')
                    raise


    def share_file(self, file_id, email, note=None):
        # check first if user already has permission
        permissions = self.list_permissions(file_id)

        for permission in permissions['permissions']:
            if 'emailAddress' in permission and permission['emailAddress'] == email and permission['role'] in ['writer', 'owner']:
                logging.debug('email already has access/owns to Google Drive file. not sharing anymore')
                return

        body = {
                'role': 'writer',
                'emailAddress': email,
                'type': 'user'
            }

        try:
            if note:
                return self.service.permissions().create(fileId=file_id, emailMessage=note, body=body).execute()
            else:
                return self.service.permissions().create(fileId=file_id, body=body).execute()
        except:
            time.sleep(2)
            try:
                if note:
                    return self.service.permissions().create(fileId=file_id, emailMessage=note, body=body).execute()
                else:
                    return self.service.permissions().create(fileId=file_id, body=body).execute()
            except:
                time.sleep(4)
                try:
                    if note:
                        return self.service.permissions().create(fileId=file_id, emailMessage=note, body=body).execute()
                    else:
                        return self.service.permissions().create(fileId=file_id, body=body).execute()
                except:
                    logging.exception('Tried to share_file in Google Drive. Tried 3 times. Still failed')
                    logging.error('email : {}'.format(email))
                    raise


    def list_permissions(self, file_id):
        try:
            return self.service.permissions().list(fileId=file_id, fields='*').execute()
        except:
            time.sleep(2)
            try:
                return self.service.permissions().list(fileId=file_id, fields='*').execute()
            except:
                time.sleep(4)
                try:
                    return self.service.permissions().list(fileId=file_id, fields='*').execute()
                except:
                    message = "Tried to list_permissions in Google Drive. Tried 3 times. Still failed"
                    logging.exception(message)
                    raise


    def remove_permission(self, file_id, permission_id):
        # transfer ownership to email
        try:
            self.service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
        except:
            time.sleep(2)
            try:
                self.service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
            except:
                time.sleep(4)
                try:
                    self.service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
                except:
                    message = "Tried to remove_permission in Google Drive. Tried 3 times. Still failed"
                    logging.exception(message)
                    raise
        return None


    def transfer_and_make_sole_owner(self, file_id, email_address):
        # list all permissions
        logging.debug('email_address : {}'.format(email_address))

        permissions = self.list_permissions(file_id)
        logging.debug('permissions : {}'.format(permissions))

        # prepare list of all users to remove after transferring ownership
        previous_owner_permission_id = None
        permission_ids_to_remove = []
        for permission in permissions['permissions']:
            if permission['role'] == 'owner':
                previous_owner_permission_id = permission['id']
            else:
                permission_ids_to_remove.append(permission['id'])

        # delete permissions of all previous users
        for permission_id in permission_ids_to_remove:
            self.remove_permission(file_id, permission_id)

        # transfer as owner
        self.transfer_ownership(file_id, email_address)

        # delete permission for this last so that we can do all the above commands.
        # otherwise, we'll get permission denied before we can complete all requests
        if previous_owner_permission_id:
            self.remove_permission(file_id, previous_owner_permission_id)


    def remove_email_from_permissions(self, file_id, email):
        # list all permissions
        permissions = self.list_permissions(file_id)

        email_permission_id = None

        # prepare list of all users to remove after transferring ownership
        permission_ids_to_remove = []
        for permission in permissions['permissions']:
            if 'emailAddress' in permission and permission['emailAddress'] == email:
                email_permission_id = permission['id']
                break

        if email_permission_id:
            self.remove_permission(file_id, email_permission_id)


    def remove_everyone_not_owner_from_permissions(self, file_id, email):
        # list all permissions
        permissions = self.list_permissions(file_id)

        system_service_account = APPENGINE_SERVICE_ACCOUNT
        system_permission_id = None

        # prepare list of all users to remove after transferring ownership
        permission_ids_to_remove = []
        for permission in permissions['permissions']:
            if 'emailAddress' in permission and permission['emailAddress'] == email:
                pass
            elif 'emailAddress' in permission and permission['emailAddress'] == system_service_account:
                system_permission_id = permission['id']
            elif permission['role'] == 'owner':
                pass
            else:
                permission_ids_to_remove.append(permission['id'])

        # delete permissions of all previous users
        try:
            for permission_id in permission_ids_to_remove:
                self.remove_permission(file_id, permission_id)
        except:
            logging.exception('error with removing permission')
            logging.debug('system_service_account : {}'.format(system_service_account))
            logging.debug('email : {}'.format(email))
            logging.debug('file_id : {}'.format(file_id))

        # delete permission for this last so that we can do all the above commands.
        # otherwise, we'll get permission denied before we can complete all requests
        if system_permission_id:
            self.remove_permission(file_id, system_permission_id)


    def share_file_to_email_address_and_remove_all_others(self, file_id, email_address, note=None):
        # list all permissions
        system_service_account = APPENGINE_SERVICE_ACCOUNT
        permissions = self.list_permissions(file_id)

        permission_ids_to_remove = []
        for permission in permissions['permissions']:
            logging.debug(permission)
            if permission['role'] == 'owner' or ('emailAddress' in permission and permission['emailAddress'] == system_service_account):
                pass
            else:
                permission_ids_to_remove.append(permission['id'])

        # delete permissions of all previous users other than previous owner
        for permission_id in permission_ids_to_remove:
            self.remove_permission(file_id, permission_id)

        # share
        self.share_file(file_id, email_address, note=note)


    def create_folder(self, folder_name, parent_id):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        try:
            return self.service.files().create(body=file_metadata, fields='id').execute()
        except:
            time.sleep(1)
            try:
                return self.service.files().create(body=file_metadata, fields='id').execute()
            except:
                time.sleep(2)
                try:
                    return self.service.files().create(body=file_metadata, fields='id').execute()
                except:
                    message = "Tried to create_folder in Google Drive. Tried 3 times. Still failed"
                    logging.exception(message)
                    raise


    def list_files_in_folder(self, folder_id):
        try:
            return self.service.files().list(q="'{}' in parents".format(folder_id), fields='*', pageSize=999).execute()
        except:
            time.sleep(1)
            return self.service.files().list(q="'{}' in parents".format(folder_id), fields='*', pageSize=999).execute()


    def search_files(self, n):
        try:
            return self.service.files().list(q="name contains '{}'".format(n), fields='*').execute()
        except:
            time.sleep(1)
            try:
                return self.service.files().list(q="name contains '{}'".format(n), fields='*').execute()
            except:
                time.sleep(1)
                try:
                    return self.service.files().list(q="name contains '{}'".format(n), fields='*').execute()
                except:
                    message = "Tried to search_files in Google Drive. Tried 3 times. Still failed"
                    logging.exception(message)
                    raise


    def get_file_name_from_drive(self, file_id):
        return self.service.files().get(fileId=file_id).execute()['name']

    
    def delete_file(self, file_id):
        logging.debug("Deleting file.")
        self.service.files().delete(fileId=file_id).execute()


    def export_file(self, file_id, mimeType):
        """
        Downloads file from drive.
        """
        logging.debug("Exporting file.")

        request = self.service.files().export_media(fileId=file_id, mimeType=mimeType)
        file_holder = io.BytesIO()
        downloader = MediaIoBaseDownload(file_holder, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()

        return file_holder





