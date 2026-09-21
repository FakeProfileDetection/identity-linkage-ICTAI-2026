"""The ten gallery-probe configurations from Table II of the paper.

Created: 2026-09-20

Every observation in the dataset is identified by a platform, a topic, and a
session.  A gallery-probe configuration says which observations are enrolled in
the gallery and which are used as probes.  Each configuration expands into
several platform-topic rotations, for example scenario 1.1 covers three
platforms times three topics, so nine rotations.  There are 171 rotations in
total across the ten configurations.

Running this file writes two things:

    python scenarios.py

  scenarios.csv         the 171 rotations, which every experiment reads
  results_template.tsv  an empty results table in the gallery-probe format,
                        which every experiment fills in and writes out

Platform, topic, and session ids follow the dataset:

    platform  1 = Facebook, 2 = Instagram, 3 = X
    topic     1 = Coach Carter, 2 = Oscar Slap, 3 = Trump/Zelensky
    session   1 = first session, 2 = second session
"""

import csv
from pathlib import Path

PLATFORM_LETTER = {1: "F", 2: "I", 3: "X"}

# Gallery platform -> probe platform, for the six ordered pairs of distinct
# platforms.  Used by scenarios 2.1, 2.2, and 3.1.
PLATFORM_PAIRS = [(1, 2), (1, 3), (2, 3), (2, 1), (3, 1), (3, 2)]

# Two gallery platforms -> one held-out probe platform.  Used by 3.2 and 4.2.
# The two scenarios list the groups in a different order.  Row order carries no
# meaning, but it is fixed so that every experiment's results table lines up
# row for row with every other.
TWO_PLATFORM_GROUPS_32 = [((1, 2), 3), ((2, 3), 1), ((3, 1), 2)]
TWO_PLATFORM_GROUPS_42 = [((1, 2), 3), ((1, 3), 2), ((2, 3), 1)]

# Gallery topic -> probe topic, for the six ordered pairs of distinct topics.
# The order differs between scenarios, and again it is fixed rather than
# meaningful.
TOPIC_PAIRS_42 = [(1, 2), (2, 3), (3, 1), (1, 3), (2, 1), (3, 2)]
TOPIC_PAIRS_51 = [(1, 2), (2, 3), (3, 1), (2, 1), (3, 2), (1, 3)]
TOPIC_PAIRS_52 = [(2, 1), (3, 2), (1, 3), (1, 2), (2, 3), (3, 1)]

BOTH_SESSIONS = (1, 2)

# Scenario id -> (variation notation from Table II, description).
# In the variation notation, factors before the dot are held constant between
# gallery and probe, and factors after it are varied.  P is platform, T is
# topic, S is session.
SCENARIO_INFO = {
    "1.1": ("PT.S", "Cross-session, same platform and topic"),
    "1.2": ("PT.S", "Cross-session, same platform and topic"),
    "2.1": ("T.PS", "Cross-platform and cross-session, same topic"),
    "2.2": ("T.PS", "Cross-platform and cross-session, same topic"),
    "3.1": ("TS.P", "Cross-platform, pooled sessions, single-platform gallery"),
    "3.2": ("TS.P", "Cross-platform, pooled sessions, two-platform gallery"),
    "4.1": ("S.PT", "Cross-platform and cross-topic, pooled sessions, single-platform gallery"),
    "4.2": ("S.PT", "Cross-platform and cross-topic, pooled sessions, two-platform gallery"),
    "5.1": ("P.TS", "Cross-topic and cross-session, same platform"),
    "5.2": ("P.TS", "Cross-topic and cross-session, same platform"),
}


def rotation_label(gallery_platforms, gallery_topics, probe_platforms, probe_topics):
    """A short name for one platform-topic rotation, ignoring session.

    Scenarios 1.1 and 1.2 reverse the session direction while keeping the same
    platforms and topics, so their rotations share a label and can be paired.
    """
    def side(platforms, topics):
        p = "".join(PLATFORM_LETTER[x] for x in platforms)
        t = "".join(f"T{x}" for x in topics)
        return f"{p}-{t}"

    return f"{side(gallery_platforms, gallery_topics)}>{side(probe_platforms, probe_topics)}"


def build_rotations():
    """Return every rotation of every scenario, in the fixed order above."""
    rows = []

    def add(scenario, gallery, probe):
        gp, gt, gs = gallery
        pp, pt, ps = probe
        rows.append({
            "scenario": scenario,
            "variation": SCENARIO_INFO[scenario][0],
            "description": SCENARIO_INFO[scenario][1],
            "rotation": rotation_label(gp, gt, pp, pt),
            "gallery_platforms": ",".join(str(x) for x in gp),
            "gallery_topics": ",".join(str(x) for x in gt),
            "gallery_sessions": ",".join(str(x) for x in gs),
            "probe_platforms": ",".join(str(x) for x in pp),
            "probe_topics": ",".join(str(x) for x in pt),
            "probe_sessions": ",".join(str(x) for x in ps),
            "gallery_samples_per_user": len(gp) * len(gt) * len(gs),
            "probe_samples_per_user": len(pp) * len(pt) * len(ps),
        })

    # 1.1 and 1.2: same platform and topic, sessions swapped.
    for scenario, (gs, ps) in [("1.1", (1, 2)), ("1.2", (2, 1))]:
        for platform in (1, 2, 3):
            for topic in (1, 2, 3):
                add(scenario,
                    ((platform,), (topic,), (gs,)),
                    ((platform,), (topic,), (ps,)))

    # 2.1 and 2.2: platform changes as well as session, topic held fixed.
    for scenario, (gs, ps) in [("2.1", (1, 2)), ("2.2", (2, 1))]:
        for gallery_platform, probe_platform in PLATFORM_PAIRS:
            for topic in (1, 2, 3):
                add(scenario,
                    ((gallery_platform,), (topic,), (gs,)),
                    ((probe_platform,), (topic,), (ps,)))

    # 3.1: platform changes, both sessions pooled on each side.
    for gallery_platform, probe_platform in PLATFORM_PAIRS:
        for topic in (1, 2, 3):
            add("3.1",
                ((gallery_platform,), (topic,), BOTH_SESSIONS),
                ((probe_platform,), (topic,), BOTH_SESSIONS))

    # 3.2: same as 3.1 but the gallery holds two platforms, which also doubles
    # the number of enrolled samples per user.
    for gallery_platforms, probe_platform in TWO_PLATFORM_GROUPS_32:
        for topic in (1, 2, 3):
            add("3.2",
                (gallery_platforms, (topic,), BOTH_SESSIONS),
                ((probe_platform,), (topic,), BOTH_SESSIONS))

    # 4.1: platform and topic both change, both sessions pooled.
    for gallery_platform in (1, 2, 3):
        for gallery_topic in (1, 2, 3):
            for probe_platform in (p for p in (1, 2, 3) if p != gallery_platform):
                for probe_topic in (t for t in (1, 2, 3) if t != gallery_topic):
                    add("4.1",
                        ((gallery_platform,), (gallery_topic,), BOTH_SESSIONS),
                        ((probe_platform,), (probe_topic,), BOTH_SESSIONS))

    # 4.2: same as 4.1 but with a two-platform gallery.
    for gallery_platforms, probe_platform in TWO_PLATFORM_GROUPS_42:
        for gallery_topic, probe_topic in TOPIC_PAIRS_42:
            add("4.2",
                (gallery_platforms, (gallery_topic,), BOTH_SESSIONS),
                ((probe_platform,), (probe_topic,), BOTH_SESSIONS))

    # 5.1 and 5.2: topic changes as well as session, platform held fixed.
    for scenario, (gs, ps), topic_pairs in [
        ("5.1", (1, 2), TOPIC_PAIRS_51),
        ("5.2", (2, 1), TOPIC_PAIRS_52),
    ]:
        for platform in (1, 2, 3):
            for gallery_topic, probe_topic in topic_pairs:
                add(scenario,
                    ((platform,), (gallery_topic,), (gs,)),
                    ((platform,), (probe_topic,), (ps,)))

    return rows


TEMPLATE_COLUMNS = ["scenario", "variation", "gallery", "gallery_samples_per_user",
                    "probe", "probe_samples_per_user", "k=1", "k=2", "k=3", "k=4", "k=5"]


def side_label(platforms, topics, sessions):
    """'F / T1 / S1' in the style of Table II."""
    p = ",".join(PLATFORM_LETTER[int(x)] for x in platforms.split(","))
    t = ",".join(f"T{x}" for x in topics.split(","))
    s = ",".join(f"S{x}" for x in sessions.split(","))
    return f"{p} / {t} / {s}"


def template_rows(rotations):
    """The results table, one row per rotation plus mean and std rows.

    An experiment fills in the five k columns for the rotation rows and writes
    the scenario mean and standard deviation into the two summary rows.
    """
    rows = [TEMPLATE_COLUMNS]
    scenarios = []
    for row in rotations:
        if row["scenario"] not in scenarios:
            scenarios.append(row["scenario"])

    for scenario in scenarios:
        for row in (r for r in rotations if r["scenario"] == scenario):
            rows.append([
                scenario,
                row["variation"],
                side_label(row["gallery_platforms"], row["gallery_topics"], row["gallery_sessions"]),
                row["gallery_samples_per_user"],
                side_label(row["probe_platforms"], row["probe_topics"], row["probe_sessions"]),
                row["probe_samples_per_user"],
                "", "", "", "", "",
            ])
        for summary in ("mean", "std"):
            rows.append([scenario, "", summary, "", "", "", "", "", "", "", ""])
    return rows


def main():
    rotations = build_rotations()
    here = Path(__file__).parent

    out = here / "scenarios.csv"
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rotations[0]))
        writer.writeheader()
        writer.writerows(rotations)

    template = here / "results_template.tsv"
    with template.open("w", newline="") as f:
        csv.writer(f, delimiter="\t").writerows(template_rows(rotations))

    counts = {}
    for row in rotations:
        counts[row["scenario"]] = counts.get(row["scenario"], 0) + 1
    print(f"Wrote {len(rotations)} rotations to {out}")
    for scenario in SCENARIO_INFO:
        print(f"  scenario {scenario}: {counts[scenario]} rotations")
    print(f"Wrote {template}")


if __name__ == "__main__":
    main()
