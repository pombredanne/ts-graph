import logging
import os

from conda_forge_tick.utils import setup_logger, load_graph

logger = logging.getLogger("conda_forge_tick.ts-graph_update_version")

# It's expected that your environment provide this info.
CONDA_FORGE_TICK_DEBUG = os.environ.get("CONDA_FORGE_TICK_DEBUG", False)


def new_update_upstream_versions(
    gx: nx.DiGraph, sources: Iterable[AbstractSource] = None
) -> None:
    # sources = ( (PyPI(), CRAN(), NPM(), ROSDistro(), RawURL(), Github()) if sources is None else sources)
    # updater = ( _update_upstream_versions_sequential if CONDA_FORGE_TICK_DEBUG else _update_upstream_versions_process_pool)

    logger.info("Updating upstream versions")
    # updater(gx, sources)


def main(args: Any = None) -> None:
    if CONDA_FORGE_TICK_DEBUG:
        setup_logger(logger, level="debug")
    else:
        setup_logger(logger)

    logger.info("Reading graph")
    # Graph enabled for inspection
    gx = load_graph()

    # call update
    new_update_upstream_versions(gx)

    logger.info("writing out file")
    with open("new_version.json", "w") as outfile:
        print(outfile)
        # this may change according to nx.DiGraph will be used or not;
        # json.dump(to_update, outfile)


if __name__ == "__main__":
    main()
