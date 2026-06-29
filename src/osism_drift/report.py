"""Grouped, narrated text rendering of drift findings.

Pure presentation, no I/O: groups actionable (non-allowlisted) DriftEntry items
by (plugin, expected_src, found_src) and renders each group as a lead sentence
(plugin.SUMMARY), the sorted name list, a Fix line (plugin.REMEDIATION), and
the two source paths (Refs). Block order follows the given `plugins` list. The
orientation header precedes the blocks. Returns [] when there are no actionable
drifts. The caller owns the stale-allowlist block and the summary.
"""

import textwrap

HEADER = "Checks follow a service's path: enabled → built → version-pinned → deployed."

_WIDTH = 76
_NAME_INDENT = "    "


def format_text(drifts, plugins):
    """Render actionable (non-allowlisted) drifts as grouped, narrated lines."""
    actionable = [d for d in drifts if not d.allowlisted]
    if not actionable:
        return []

    by_name = {p.NAME: p for p in plugins}
    order = {p.NAME: i for i, p in enumerate(plugins)}

    groups = {}
    for d in actionable:
        groups.setdefault((d.plugin, d.expected_src, d.found_src), []).append(d)

    out = [HEADER, ""]
    for key in sorted(groups, key=lambda k: (order.get(k[0], len(order)), k[1], k[2])):
        plugin_name, expected_src, found_src = key
        out.extend(
            _format_group(by_name[plugin_name], expected_src, found_src, groups[key])
        )
    return out


def _format_group(plugin, expected_src, found_src, entries):
    """Render one (plugin, expected_src, found_src) group as text lines."""
    names = sorted(d.image for d in entries)

    # A group shares one (expected_src, found_src); entries in it carry the
    # same summary/remediation. Take the first's override, else the plugin's.
    first = entries[0]
    summary = first.summary if first.summary is not None else plugin.SUMMARY
    remediation = (
        first.remediation if first.remediation is not None else plugin.REMEDIATION
    )

    lead = f"{plugin.NAME} — {summary.format(n=len(names))}"
    lines = list(
        textwrap.wrap(
            lead, width=_WIDTH, break_long_words=False, break_on_hyphens=False
        )
    )
    lines.append("")
    lines.extend(
        textwrap.wrap(
            ", ".join(names),
            width=_WIDTH,
            initial_indent=_NAME_INDENT,
            subsequent_indent=_NAME_INDENT,
            break_long_words=False,
            break_on_hyphens=False,
        )
    )
    lines.append("")
    lines.extend(
        textwrap.wrap(
            f"Fix: {remediation}",
            width=_WIDTH,
            initial_indent="  ",
            subsequent_indent="       ",
            break_long_words=False,
            break_on_hyphens=False,
        )
    )
    lines.append(f"  Refs: {expected_src}")
    lines.append(f"        {found_src}")
    lines.append("")
    return lines
