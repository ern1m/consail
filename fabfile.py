from fabric import Connection, task
from invoke import Exit
from invoke import run as local
from termcolor import colored, cprint

# http://docs.pyinvoke.org/en/latest/concepts/invoking-tasks.html#task-command-line-arguments
project_name = "cs_api"


def get_connection(env):
    envs = {"dev": Connection(host="siema.consail.site", user="ubuntu")}
    try:
        return envs[env]
    except KeyError:
        msg = f"{env} is not valid env. Available envs: {', '.join(envs.keys())}"
        raise Exit(colored(msg, "red"))


@task
def deploy(ctx, env):
    cprint("Creating code archive..", "cyan")
    code_archive = f"{project_name}.tar.gz"
    local(f"git archive --format=tar.gz HEAD > {code_archive}")

    with get_connection(env) as c:
        cprint("Copying code to server..", "cyan")
        c.put(code_archive, remote=f"{code_archive}")
        local(f"rm {code_archive}")

        cprint("Extracting code..", "cyan")
        c.run(f"mkdir -p webapp && tar xmzf {code_archive} -C webapp")

        cprint("Copying secrets..", "cyan")
        c.run(f"rsync -r ~/.envs/.{env} ~/webapp/.envs/")

        compose_runner = c.run  # run it on remote machine
        with c.cd("~/webapp/"):
            cprint("Running docker containers..", "cyan")
            docker_compose(compose_runner, env, "build")
            docker_compose(compose_runner, env, "stop")
            docker_compose(
                compose_runner, env, "run --rm django python manage.py migrate"
            )
            docker_compose(
                compose_runner,
                env,
                "run --rm django python manage.py collectstatic --noinput",
            )
            docker_compose(
                compose_runner, env, "up -d django celeryworker celerybeat nginx"
            )


def docker_compose(runner, env, command):
    # runner could be
    # - c.run - run on remote machine specified by ssh Connection params
    # - c.local - runs on local machine
    cmd = f"docker-compose -p {project_name}_{env} -f {env}.yml {command}"
    cprint(cmd, "green")
    runner(cmd)
