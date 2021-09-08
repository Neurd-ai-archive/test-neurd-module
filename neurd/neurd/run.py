import git, pathlib, shutil
import os, errno

BASEDIR = pathlib.Path(__file__).parent

# Neurd defined vars
NEURD_CONFIG_FILEPATH = BASEDIR + '/neurd.conf.py'
NEURD_DOCKERFILE_FILEPATH = BASEDIR + '/Dockerfile'
NEURD_CONTAINER_SERVICE_PATH = BASEDIR + '/_neurd_container_server'

# USERDEF vars
GIT_REPO_NAME = 'TEST-REPO'
TARGET_DIR = './TESTING-TARGET-DIR'
GIT_REPO_ADDRESS = 'git@github.com:preller/Best-README-Template.git'
USER_DEFINED_PROCESS_FILE = BASEDIR + '/PROCESS.py'



def append_new_line(file_name, text_to_append): # Append given text as a new line at the end of file #Adapted https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
# Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def gcloud_build_push(): #TBD, should use the gcloud api container (we'll create and endpoint)
    return 'url'

def make_dir(path_to_dir):
    try:
        os.makedirs(path_to_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def updateDirs():
    #STEP Clone a repo locally (later/now all this will be a container)
    # Check if URL is https or ssh automatically
    # Check out via HTTPS 
    # git.Repo.clone_from('https://github.com/DevDungeon/Cookbook', 'Cookbook-https')
    # or clone via ssh (will use default keys) #Adapted https://www.devdungeon.com/content/working-git-repositories-python#toc-9
    git.Repo.clone_from(GIT_REPO_ADDRESS, './' + GIT_REPO_NAME)

    #STEP Check that there is a Dockerfile file and a neurd.conf.py file and where the user sets the parameters needed; if so, continue
    if not pathlib.Path(NEURD_CONFIG_FILEPATH).is_file() or not pathlib.Path(NEURD_DOCKERFILE_FILEPATH).is_file():
        return False

    #STEP Create an app directory with the flask and flask-restful app, 
    # exposing a /process endpoint that receives a POST request with all the data required in a json (image + data, for instance); 
    # you can use the one already done, delete extra stuff, and make it use environmental variables for user-defined parameters 
    # (input, output, process method file to call something like os.environ.get("USER_DEFINED_PROCESS_FILE").process(INPUT_FILEPATH, OUTPUT_FILEPATH)


    #STEP Create the gunicorn.sh file (same as example)

    #STEP Create the gunicorn.conf.py file (same as example)
    shutil.copytree('./_neurd_container_server', TARGET_DIR)

    #STEP Add the Dockerfile requirements (mainly set environmental variables and entrypoint file to gunicorn)
    append_new_line(NEURD_DOCKERFILE_FILEPATH, 'ENTRYPOINT ["./gunicorn.sh"]') #TODO Later it should be copied from a file, easier to maintain, and env files should be there too
    #STEP Add the environmental variables set by the user (validated and everthing, can be done later)
    append_new_line(NEURD_DOCKERFILE_FILEPATH, 'ENV TEST_ENV_VAR=1')

    #STEP Call the gcloud API to build+push this (we can create that endpoint easily later), which returns some info ("OK" "ERROR" etc, and also the url path of the built image in gcr.io)
    image_url = gcloud_build_push() #TBD, should use the gcloud api container (we'll create and endpoint)

    #STEP Return this url from the previous step (later on, a neurd-owned URL redirector we create, not the gcr.io)
    return image_url


if __name__ == "__main__":
    updateDirs()
