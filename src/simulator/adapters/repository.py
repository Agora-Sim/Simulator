# ================================================================
# 0. Section: IMPORTS
# ================================================================
from ruamel.yaml import YAML
from dataclasses import dataclass
from pathlib import Path

from .source import Source


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Repository:
    source: Source

    _config_path: Path = Path("src/simulator/adapters/configs/config.yaml")

    def init_simulation(self) -> Path:
        self.source.base_folder.mkdir(parents=True, exist_ok=True)
        self.source.folder.mkdir(parents=True, exist_ok=True)
        self.source.runs_folder.mkdir(parents=True, exist_ok=True)

        # 2. Make a copy of config.yaml into the folder
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)

        # 3. Loads the default yaml
        with open(self._config_path, "r", encoding="utf-8") as f:
            config = yaml.load(f)

        # 4. Updates the config with source information
        config["simulation_name"] = self.source.simulation_name
        config["simulation_description"] = self.source.simulation_description

        # 5. Saves the updated config to the pipeline folder
        with open(self.source.config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f)

        return self.source.folder

    def init_run(self) -> tuple[Path, int]:
        nr_of_runs = len(list(self.source.runs_folder.iterdir()))
        run_id = nr_of_runs + 1
        run_id_str = str(run_id)

        run_folder = self.source.get_run_folder(run_id_str)
        run_folder.mkdir(parents=True, exist_ok=True)

        return run_folder, run_id

    def init_figures(self) -> Path:
        figures_folder = self.source.figures_folder
        figures_folder.mkdir(parents=True, exist_ok=True)

        return figures_folder
