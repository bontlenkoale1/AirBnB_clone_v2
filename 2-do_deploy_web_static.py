#!/usr/bin/env bash
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['18.209.180.39', '54.160.95.41']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school' 


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "web_static_{}.tgz".format(now)
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(file_name))
        return "versions/{}".format(file_name)
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_filename = archive_path.split('/')[-1]
        release_folder = "/data/web_static/releases/{}".format(archive_filename[:-4])
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_folder))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move contents of web_static to the release folder
        run("mv {}/web_static/* {}".format(release_folder, release_folder))

        # Remove the web_static symbolic link
        run("rm -rf {}/web_static".format(release_folder))

        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version of your code
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")

        return True
    except Exception:
        return False
