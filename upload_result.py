# -*- coding: utf-8 -*-
import os
import platform
import json
from shutil import copyfile

REMOTE_ADDR = "https://github.com/emputi-osp/Minecraft-Education-Result.git"
JAVA_SOURCE_FILE = '/project/src/main/java/io/github/emputi/MinecraftEducation.java'

def execute_git(nickname, group):
    os.chdir('./.gitproject')
    import git
    if not os.path.exists(os.getcwd() + "/.git"):
        repo = git.Repo.init('./', True)
        print "Initialized git repository."
        git.Remote.add(repo, "origin", REMOTE_ADDR)
        print "Git remoted -> " + REMOTE_ADDR
    
    g = git.Git('./')
    print "Updating changed of project repository ..."
    g.pull('origin', 'master')
    print "Updating changed project repository ...Done"
    repo = git.Repo("./")
    
    if not os.path.exists(".." + JAVA_SOURCE_FILE):
        print "Error! {} doesn't exist. Please check file is exist.".format(JAVA_SOURCE_FILE)
        return
    dst = "{}/{}/{}".format(group, nickname, "MinecraftEducation.java")
    copyfile(".." + JAVA_SOURCE_FILE, dst)

    result = g.execute(["git", "add", dst])
    try:
        repo.git.commit('-m', '"Auto-committed from MinecraftEducation-Uploader [{}@{}]"'.format(nickname, group), author=nickname)
    except git.exc.GitCommandError:
        pass

    print "Committed file to project repository."
    
    origin = repo.remote(name='origin')
    print "Pushing your changed file ..."
    repo.git.push('--set-upstream', origin, "master")
    
    print "Pushing your changed file ...Done"
    print "Task finished"
    if platform.system() == "Windows":
        os.system('pause')

def main():
    print "Git Automation uploader for Minecraft-education"
    print "Copyright 2019, ruskonert(ruskonert@gmail.com) all rights reserved."
    try:
        import git
    except ImportError:
        print "Oh, You have not GitPython module, Please install this module"
        return
    
    json_data = open('./settings.json').read()
    json_tree = json.loads(json_data)

    nickname = json_tree['nickname']
    group = json_tree['group']

    if not nickname or nickname == "Here is your name":
        print "오류: 닉네임이 지정되지 않았습니다. 닉네임을 지정해주세요."
        if platform.system() == "Windows":
            os.system('pause')
        return
    
    if not group or group == "example":
        print "오류: 그룹이 지정되지 않았습니다. 그룹을 지정해주세요."
        if platform.system() == "Windows":
            os.system('pause')
        return
    if not os.path.exists('./.gitproject'):
        os.mkdir('./.gitproject')
    execute_git(nickname, group)

if __name__ == "__main__":
    main()