#!/usr/bin/python3
# pylint: disable=R,C,W,E

import udemy.widevine_pssh_pb2 as widevine_pssh_pb2
import udemy.mp4parse as mp4parse
import codecs
import base64
import os
import json

with open(os.path.join(os.getcwd(), "keyfile.json"), 'r') as keyfile:
    keyfile = keyfile.read()
keyfile = json.loads(keyfile)


WIDEVINE_SYSTEM_ID = "edef8ba979d64acea3c827dcd51d21ed"


def extract_pssh(filepath):
    """
    Parameters
    ----------
    filepath : str
        file path with a PSSH header
    Returns
    -------
    String
    """

    boxes = mp4parse.F4VParser.parse(filename=filepath)
    for box in boxes:
        if box.header.box_type == 'moov':
            pssh_box = next(x for x in box.pssh if x.system_id ==
                            WIDEVINE_SYSTEM_ID)
            hex = codecs.decode(pssh_box.payload, "hex")

            pssh = widevine_pssh_pb2.WidevinePsshData()
            pssh.ParseFromString(hex)
            content_id = base64.b16encode(pssh.content_id)
            return content_id.decode("utf-8")
    return None


def decrypt(kid, encrypted_filepath, decrypted_filepath):
    """
    @author Jayapraveen
    """
    try:
        key = keyfile[kid.lower()]
        if (os.name == "nt"):
            os.system(f"mp4decrypt --key 1:%s \"%s\" \"%s\"" %
                      (key,
                       encrypted_filepath,
                       decrypted_filepath))
        else:
            os.system(f"nice -n 7 mp4decrypt --key 1:%s \"%s\" \"%s\"" %
                      (key,
                       encrypted_filepath,
                       decrypted_filepath))
    except KeyError:
        raise KeyError("Key not found")


def mux(decrypted_video_filepath, decrypted_audio_filepath, merged_filepath):
    """
    @author Jayapraveen
    """
    print(decrypted_video_filepath, decrypted_audio_filepath, merged_filepath)
    if os.name == "nt":
        command = f"ffmpeg -y -i \"{decrypted_video_filepath}\" -i \"{decrypted_audio_filepath}\" -c copy \"{merged_filepath}\""
    else:
        command = f"nice -n 7 ffmpeg -y -i \"{decrypted_video_filepath}\" -i \"{decrypted_audio_filepath}\" -c copy \"{merged_filepath}\""
    retCode = os.system(command)
    if retCode == 0:
        return True
    else:
        return False
