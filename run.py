#!env python

import os
import subprocess
import sys
import shlex

def sanitize(key_name):
    v = os.environ.get(f"INPUT_{key_name}")
    if not v:
        raise Exception(f"Unable to find the {key_name}. Did you set {key_name}?")
    return v

def aws_configure(key_id, key_secret, region):
    os.environ['AWS_ACCESS_KEY_ID'] = key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = key_secret
    os.environ['AWS_DEFAULT_REGION'] = region

def ecr_login(region):
    get_login = subprocess.Popen(['aws', 'ecr', 'get-login', '--no-include-email', '--region', region], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    login_command, stderr = get_login.communicate()
    if stderr:
        print(stderr.decode('utf-8'))
    cmd = shlex.split(login_command.decode('utf-8').strip())
    print(cmd)
    docker_login = subprocess.Popen(cmd, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    result, stderr = docker_login.communicate()
    if stderr:
        print(stderr.decode('utf-8'))
    print(result.decode('utf-8'))


def tag(account_url, repo, tag):
    return f"{account_url}/{repo}:{tag}"

def evaluate_tags(account_url, repo, raw_tags):
    tokens = raw_tags.strip().split(",")
    tags = []
    for token in tokens:
        stripped_token = token.strip()
        if stripped_token[0] != "%":
            tags.append(tag(account_url, repo, stripped_token))
            continue
        cmd = shlex.split(stripped_token[1:])
        tag_eval = subprocess.Popen(cmd, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
        result, stderr = tag_eval.communicate()
        if stderr:
            print(stderr.decode('utf-8'))
            continue
        t = result.decode('utf-8').strip()
        tags.append(tag(account_url, repo, t))

    return tags

def docker_build(tags, path, dockerfile_path="Dockerfile", extra_build_args=""):
    tag_args = []
    for tag in tags:
        print(f"Building for {tag}")
        tag_args += ["-t", tag]

    command = ["docker", "build"] \
        + ([] if extra_build_args == "" else extra_build_args.split(' ')) \
        + ["-f", dockerfile_path] \
        + tag_args \
        + [path]
    print(command)
    build = subprocess.Popen(command, 
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE)
    for line in iter(build.stdout.readline, b''):
        sys.stdout.write(line.decode('utf-8'))


def docker_push_to_ecr(tags):
    for tag in tags:
        print(f"Pushing {tag}")
        command = ["docker", "push", tag]
        push = subprocess.Popen(command, 
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE)
        for line in iter(push.stdout.readline, b''):
            sys.stdout.write(line.decode('utf-8'))
        print(f"Pushed {tag} !")
        
    

def main():
    access_key_id = sanitize("ACCESS_KEY_ID")
    secret_access_key = sanitize("SECRET_ACCESS_KEY")
    region = sanitize("REGION")
    account_id = sanitize("ACCOUNT_ID")
    repo = sanitize("REPO")
    path = sanitize("PATH")
    raw_tags = sanitize("TAGS")
    dockerfile_path = sanitize("DOCKERFILE")
    extra_build_args = ""
    account_url=f"{account_id}.dkr.ecr.{region}.amazonaws.com"

    aws_configure(access_key_id, secret_access_key, region)
    ecr_login(region)
    tags = evaluate_tags(account_url, repo, raw_tags)
    # print(tags)

    docker_build(tags, path, dockerfile_path=dockerfile_path, extra_build_args=extra_build_args)
    docker_push_to_ecr(tags)

main()