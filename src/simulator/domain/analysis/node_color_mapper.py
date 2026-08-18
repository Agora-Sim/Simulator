# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass

from ..node import Node
from ..modules import NodeModule
from .node_color_spec import NodeColorSpec
from ..simulation_state import SimulationState


# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class NodeColorMapper:
    spec: NodeColorSpec

    def values(self, state: SimulationState) -> dict[int, float]:
        result: dict[int, float] = {}
        for node in state.nodes:
            if node.node_type != self.spec.node_type or not node.status:
                continue

            module = self._find_module(node)
            if module is None:
                continue
            result[node.id] = float(getattr(module, self.spec.variable))
        return result


    # ──────────────────────────────────────────────────────
    # 1.1 Subsection: Helper Functions
    # ──────────────────────────────────────────────────────
    def _find_module(self, node: Node) -> NodeModule | None:
        # 1. Module identity is the ClassVar name, not the dataclass fields
        return next((m for m in node.modules if m.name == self.spec.module_name), None)
