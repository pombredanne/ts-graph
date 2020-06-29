import json
import subprocess
import logging
import tqdm
import networkx as nx
from .utils import load_graph, executor

# conda-forge logger
logger = logging.getLogger("conda-forge-tick._bad_issues_request")


# prepare subprocess run command
def hub_create_issue(name: str, maintainer: any, bad_str: any) -> None:
    # TODO: maybe add a way to create the issue at the feedstock page, not inside cf-scripts
    title = f"Bad feedstock error on Conda-forge ({name})"
    label1 = "conda-forge"
    label2 = "bad"
    body = (
        "An bad error occurred when trying to update your feedstock information, "
        "please check any possible alteration made.\n I the project was discontinued please let us know.\n"
    )
    body += (
        f"You are receiving this error as an attempt to solve the current bad behavior "
        f"with the actual version of your feedstock, the problem raised {bad_str} as exception "
        f"for retrieving a new version, please look for further details at..."
    )

    assignee = f"{maintainer}"
    command = "gh issue create"
    command += f'--title "{title}" --body "{body}" --label "{label1}" --label "{label2}" --assignee "{assignee}"'
    try:
        # try GitHub cli issue creation
        subprocess.run(command)
    except Exception as ee:
        logging.info("")
    else:
        pass


def hub(gx: nx.DiGraph) -> None:
    # Open the data file with feedstock bad relating information
    with open("bad.json") as file:
        # bad_data is a dict containing info regarding the Node feedstock and it's bad status
        bad_data = json.load(file)

    _all_nodes = [t for t in gx.nodes.items()]
    revision = []
    for node, node_attrs in _all_nodes:
        with node_attrs["payload"] as attrs:
            if node in bad_data:
                revision.append((node, attrs))

    with executor(kind="dask", max_workers=20) as pool:
        for node, node_attrs in tqdm.tqdm(revision):
            with node_attrs["payload"]["extra"] as attrs_extra:
                # TODO: This will not work, we need to send a new issue for every maintainers not stack them
                # get maintainers list
                maintainers = attrs_extra.get("recipe-maintainers")

                # get bad occurrence
                bad = bad_data[f"{node}"]
                pool.submit(hub_create_issue, node, maintainers, bad)


if __name__ == "__main__":
    # load graph
    gx = load_graph()

    # load feedstock info and try issue request
    try:
        hub(gx)
    except Exception as e:
        pass
