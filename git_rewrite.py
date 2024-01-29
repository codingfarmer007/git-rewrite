import os, sys, shutil, subprocess

def git_cmd(cmd, cur_dir, cur_env=None):
    cmds = ['git']
    cmds.extend(cmd)
    r = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cur_dir, env=cur_env)
    out, err = r.communicate()
    output = (err if len(err) else out).decode()
    print(cmds)
    print(output)
    return output

def git_copy_repo(origin, copyed, ignored = ['.git']):
    targets = os.listdir(copyed)
    for target in targets:
        if target in ignored:
            continue
        
        targte_path = os.path.join(copyed, target)
        if os.path.isdir(targte_path):
            shutil.rmtree(targte_path)
        else:
            os.remove(targte_path)
    
    sources = os.listdir(origin)
    for source in sources:
        if source in ignored:
            continue
        
        source_path = os.path.join(origin, source)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, os.path.join(copyed, source))
        else:
            shutil.copyfile(source_path, os.path.join(copyed, source))

def git_clear_repo(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    
    if not os.path.exists(dir):
        os.makedirs(dir)

if '__main__' == __name__:
    origin_git_root = sys.argv[1] if len(sys.argv) > 1 else '.\\project'
    target_git_root = sys.argv[2] if len(sys.argv) > 2 else origin_git_root + '-copyed'
    user_name       = sys.argv[3] if len(sys.argv) > 3 else 'newcodingfarmer'
    user_email      = sys.argv[4] if len(sys.argv) > 4 else 'newcodingfarmer@gmail.com'

    git_clear_repo(target_git_root)
    git_cmd(['init'], target_git_root)
    git_cmd(['config', 'user.name', user_name], target_git_root)
    git_cmd(['config', 'user.email', user_email], target_git_root)
    
    commit_list = git_cmd(['log', '--pretty=oneline', '--reverse'], origin_git_root).splitlines()
    for commit in commit_list:
        id, comment = commit.split(' ', 1)
        date = git_cmd(['log', '--pretty=format:"%cd"', id, '-1'], origin_git_root)
        git_cmd(['checkout', id], origin_git_root)
        git_copy_repo(origin_git_root, target_git_root, ['.git', 'library'])
        git_cmd(['add', '.'], target_git_root)
        git_cmd(['commit', '-m', comment], target_git_root)
        git_cmd(['commit', '--amend', '--no-edit', '--date='+ date], target_git_root, {'GIT_COMMITTER_DATE':date})
    
    print('done')