"""Scale OBJ vertex data so the longest axis matches a target size in UE centimeters.

Unreal treats imported mesh units as centimeters (uu) at actor scale 1. Many web
assets (Kenney, etc.) author in meters with small numeric coordinates, so a direct
import yields dollhouse-sized meshes.

Kenney OBJ assets use Y-up with forward along +Z. Unreal uses Z-up with forward
along +X. Use --kenney-ue to remap axes, apply a +180° Z correction (Kenney
forward lands on -X without it), reverse face winding (fixes inverted normals
from the odd axis permutation), then scale.

Usage:
  python scale_obj_to_ue_cm.py input.obj output.obj --target-max-cm 90 --kenney-ue
  python scale_obj_to_ue_cm.py input.obj --report-only --kenney-ue

After scaling, import the output OBJ with StaticMeshTools.import_file and spawn
the actor at scale 1 with rotation 0.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

Vertex = tuple[float, float, float]

VERTEX_RE = re.compile(
    r"^v\s+(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+"
    r"(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+"
    r"(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)"
)
NORMAL_RE = re.compile(
    r"^vn\s+(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+"
    r"(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+"
    r"(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)"
)
FACE_RE = re.compile(r"^f\s+(.+)$")


def kenney_to_ue(x: float, y: float, z: float) -> Vertex:
    """Kenney OBJ (Y-up, forward +Z) -> UE (Z-up, forward +X). Height on +Z."""
    ue_x, ue_y, ue_z = z, -x, y
    return -ue_x, -ue_y, ue_z


def vertex_bounds(vertices: list[Vertex]) -> tuple[float, float, float]:
    mins = [float("inf")] * 3
    maxs = [float("-inf")] * 3
    for x, y, z in vertices:
        mins[0] = min(mins[0], x)
        mins[1] = min(mins[1], y)
        mins[2] = min(mins[2], z)
        maxs[0] = max(maxs[0], x)
        maxs[1] = max(maxs[1], y)
        maxs[2] = max(maxs[2], z)
    return tuple(maxs[i] - mins[i] for i in range(3))


def max_extent(spans: tuple[float, float, float]) -> float:
    return max(spans)


def read_vertices(path: Path, *, kenney_ue: bool) -> list[Vertex]:
    vertices: list[Vertex] = []
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = VERTEX_RE.match(line)
            if not match:
                continue
            x, y, z = (float(match.group(i)) for i in range(1, 4))
            if kenney_ue:
                x, y, z = kenney_to_ue(x, y, z)
            vertices.append((x, y, z))
    if not vertices:
        raise ValueError(f"No vertices found in {path}")
    return vertices


def reverse_face_line(line: str) -> str:
    match = FACE_RE.match(line)
    if not match:
        return line
    parts = match.group(1).split()
    parts.reverse()
    return "f " + " ".join(parts) + ("\n" if line.endswith("\n") else "")


def write_obj(
    src: Path,
    dst: Path,
    *,
    kenney_ue: bool,
    factor: float,
) -> None:
    lines: list[str] = []
    with src.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            vmatch = VERTEX_RE.match(line)
            if vmatch:
                x, y, z = (float(vmatch.group(i)) for i in range(1, 4))
                if kenney_ue:
                    x, y, z = kenney_to_ue(x, y, z)
                x, y, z = x * factor, y * factor, z * factor
                lines.append(f"v {x:.6f} {y:.6f} {z:.6f}\n")
                continue
            nmatch = NORMAL_RE.match(line)
            if nmatch and kenney_ue:
                nx, ny, nz = (float(nmatch.group(i)) for i in range(1, 4))
                nx, ny, nz = kenney_to_ue(nx, ny, nz)
                lines.append(f"vn {nx:.6f} {ny:.6f} {nz:.6f}\n")
                continue
            if kenney_ue and line.startswith("f "):
                lines.append(reverse_face_line(line))
                continue
            lines.append(line)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8", newline="\n") as handle:
        handle.writelines(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument(
        "--target-max-cm",
        type=float,
        help="Longest axis after import should be this many UE centimeters (uu).",
    )
    parser.add_argument(
        "--kenney-ue",
        action="store_true",
        help="Kenney Y-up/+Z-forward -> UE Z-up/+X-forward; reverse face winding.",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Print source bounds and exit without writing output.",
    )
    args = parser.parse_args()

    vertices = read_vertices(args.input, kenney_ue=args.kenney_ue)
    spans = vertex_bounds(vertices)
    extent = max_extent(spans)
    print(f"source: {args.input}")
    if args.kenney_ue:
        print("axis remap: Kenney Y-up/+Z-forward -> UE Z-up/+X-forward")
    print(f"spans (effective units): x={spans[0]:.6f} y={spans[1]:.6f} z={spans[2]:.6f}")
    print(f"max extent: {extent:.6f}")
    print(f"imported at actor scale 1 (uu ~= cm): max ~{extent:.3f} cm")

    if args.report_only:
        return

    if args.output is None:
        parser.error("output path required unless --report-only is set")
    if args.target_max_cm is None:
        parser.error("--target-max-cm is required when writing output")
    if not args.kenney_ue:
        parser.error("--kenney-ue is required when writing output")

    if extent <= 0:
        raise ValueError("Mesh has zero extent; cannot scale.")

    factor = args.target_max_cm / extent
    write_obj(args.input, args.output, kenney_ue=True, factor=factor)
    out_spans = tuple(s * factor for s in spans)
    print(f"scale factor: {factor:.6f}")
    print(f"output: {args.output}")
    print(f"expected max extent after import: {max_extent(out_spans):.3f} cm")
    print(f"expected spans after import: x={out_spans[0]:.1f} y={out_spans[1]:.1f} z={out_spans[2]:.1f} cm")


if __name__ == "__main__":
    main()