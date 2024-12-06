"""Generate a synthetic example 3D+t dataset following the fUSI-BIDS v0.0.10 draft."""

import datetime
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

fusi_bids_version = "0.0.10"

rawdata_path = Path("./datasets") / fusi_bids_version
rawdata_path.mkdir(parents=True, exist_ok=True)

# The dataset description JSON file is mandatory.
dataset_description_path = rawdata_path / "dataset_description.json"
dataset_description = {
    "Name": f"fUSI-BIDS v{fusi_bids_version} example 3D+t dataset",
    "BIDSVersion": "1.10.0",
    "DatasetType": "raw",
    "Authors": ["Samuel Le Meur-Diebolt"],
    "GeneratedBy": [
        {
            "Name": "Custom script",
            "Description": "Custom Python script used to convert machine output to BIDS.",
        }
    ],
}

with open(dataset_description_path, "w") as dataset_description_file:
    dataset_description_file.write(json.dumps(dataset_description, indent=2))

# The README file should describe the dataset and how to use it.
readme_path = rawdata_path / "README.md"
readme = f"""# Example fUSI-BIDS v{fusi_bids_version} dataset

This dataset provides an example for version {fusi_bids_version} of the [fUSI-BIDS
specification](https://docs.google.com/document/d/1W3z01mf1E8cfg_OY7ZGqeUeOKv659jCHQBXavtmT-T8/edit?pli=1#heading=h.4k1noo90gelw).

## Overwiew

This dataset consists of ten subjects, each with two sessions: vehicle and treatment.
Each session includes:

- a 3D angiography,
- three 2D+t functional scans with visual stimulation at three different probe poses,
- one 3D+t functional scan in awake condition with four different probe poses.

All data files are empty and only serve as an example of the fUSI-BIDS structure.

## Authors

- [Samuel Le Meur-Diebolt](mailto:samuel@diebolt.io)"""

with open(readme_path, "w") as readme_file:
    readme_file.write(readme)

# The CHANGES file should describe the different versions of the dataset. It must follow
# the CPAN Changelog convention: https://metacpan.org/release/HAARG/CPAN-Changes-0.400002/view/lib/CPAN/Changes/Spec.pod
changes_path = rawdata_path / "CHANGES.md"
changes = """1.0.0 2024-12-06
  
 - Initial release."""

with open(changes_path, "w") as changes_file:
    changes_file.write(changes)

# The participants.tsv file should describe properties of the participants, such as age,
# sex, and strain.
participants_table_path = rawdata_path / "participants.tsv"
participants_table = {
    "participant_id": [f"sub-{i:02d}" for i in range(1, 11)],
    "species": ["mus musculus"] * 10,
    "strain_identifier": ["C57BL/6J"] * 10,
    "age": rng.integers(25, 30, size=(10,)).tolist(),
    "sex": rng.choice(["F", "M"], size=10),
    "weight": 2 * rng.standard_normal(10),
}
participants_table = pd.DataFrame(participants_table)

participants_table.loc[participants_table.sex == "F", "weight"] += 26
participants_table.loc[participants_table.sex == "M", "weight"] += 35

participants_table.to_csv(participants_table_path, sep="\t", index=False)

participants_json_path = rawdata_path / "participants.json"
participants_json = {
    "species": {
        "Description": "binomial species name from NCBI Taxonomy (https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi)"
    },
    "strain": {"Description": "string value indicating the strain of the species"},
    "strain_identifier": {
        "Description": "string value indicating a strain identifier (e.g. RRID or ILAR)."
    },
    "age": {"Description": "Age of the animal at first acquisition, in weeks."},
    "sex": {"Description": "Sex of the animal", "Levels": {"M": "male", "F": "female"}},
    "weight": {"Description": "Weight of the animal at first acquisition, in grams."},
}

with open(participants_json_path, "w") as participants_json_file:
    participants_json_file.write(json.dumps(participants_json, indent=2))

# All power Doppler scans have common metadata: system manufacturer, model, software
# version, etc. We can use BIDS' inheritance principle to store this information in a
# common sidecar JSON file at the root of the dataset.
common_pwd_json = {
    "Manufacturer": "Iconeus",
    "ManufacturersModelName": "Iconeus One",
    "DeviceSerialNumber": "X23HFB12K8",
    "StationName": "Machine01",
    "SoftwareVersions": "1.5.0",
    "ProbeType": "linear",
    "ProbeModel": "IcoPrime",
    "ProbeCentralFrequency": 15.625,
    "ProbeNumberOfElements": 128,
    "ProbePitch": 0.11,
    "ProbeRadiusOfCurvature": 0,
    "ProbeElevationAperture": 1.5,
    "ProbeElevationFocus": 8,
    "Depth": [1, 10],
    "UltrasoundPulseRepetitionFrequency": 5500,
    "PlaneWaveAngles": [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10],
    "UltrafastSamplingFrequency": 500,
    "ProbeVoltage": 25,
    "SequenceName": "default",
    "ClutterFilterWindowDuration": 400,
    "ClutterFilters": [
        {
            "FilterType": "Butterworth low-pass",
            "HighThreshold": 25,
        },
        {"FilterType": "Fixed-threshold SVD", "LowThreshold": 60, "HighThreshold": 200},
    ],
    "PowerDopplerIntegrationDuration": 400,
}

common_pwd_json_path = rawdata_path / "pwd.json"
with open(common_pwd_json_path, "w") as pwd_json_file:
    pwd_json_file.write(json.dumps(common_pwd_json, indent=2))

# Timing of events for task-based acquitions are stored in TSV files with `events`
# suffix. In this example dataset, we assume that all task-based acquisitions have the
# same stimulus paradigm. Therefore, a single `events.tsv` file is created at the root
# of the dataset.
events = {
    "onset": np.arange(30, 630, 60).tolist(),
    "duration": [30] * 10,
}
pd.DataFrame(events).to_csv(
    rawdata_path / "task-stim_events.tsv", sep="\t", index=False
)

# Invidual data files are created as empty NIfTI files. Task metadata are stored as
# sidecar JSON files next to each NIfTI file: we cannot create a root-level task JSON
# file since it would violate rule 4 of the BIDS inheritance principle (we already have
# a common pwd.json file at the root of the dataset).
tasks_json = {
    "awake": {
        "TaskName": "awake",
        "TaskDescription": "Awake head-fixed state.",
        "RepetitionTime": 2.4,
        "DelayAfterTrigger": 0,
    },
    "stim": {
        "TaskName": "stim",
        "TaskDescription": "Visual stimulation task.",
        "RepetitionTime": 0.4,
    },
}

sessions = ("vehicle", "treatment")
acq_values = ("bregmaMinus2", "bregmaMinus1", "bregmaPlus05")
n_probe_poses = 4
for subject_index in range(1, 11):
    subject_path = rawdata_path / f"sub-{subject_index:02d}"
    subject_path.mkdir(exist_ok=True)

    session_dates = []
    for session in sessions:
        session_path = subject_path / f"ses-{session}"

        # Angiographic scans.
        angio_path = session_path / "angio"
        angio_path.mkdir(exist_ok=True, parents=True)

        angio_scan_path = (
            angio_path / f"sub-{subject_index:02d}_ses-{session}_pwd.nii.gz"
        )
        angio_scan_path.touch()
        scan_paths_in_session = [str(angio_scan_path.relative_to(session_path))]

        # Functional scans.
        fusi_path = session_path / "fus"
        fusi_path.mkdir(exist_ok=True, parents=True)

        # Stimulus task scans.
        for acq_value in acq_values:
            fusi_scan_path = fusi_path / (
                f"sub-{subject_index:02d}_ses-{session}_task-stim"
                f"_acq-{acq_value}_pwd.nii.gz"
            )
            fusi_scan_path.touch()
            scan_paths_in_session.append(str(fusi_scan_path.relative_to(session_path)))

            # Sidecar JSON file storing task metadata and volume timings.
            sidecar_json_path = fusi_scan_path.with_suffix("").with_suffix(".json")
            with open(sidecar_json_path, "w") as sidecar_json_file:
                sidecar_json_file.write(json.dumps(tasks_json["stim"], indent=2))

        # Awake task scans.
        for pose_index in range(1, n_probe_poses + 1):
            fusi_scan_path = fusi_path / (
                f"sub-{subject_index:02d}_ses-{session}_task-awake"
                f"_pose-{pose_index:02d}_pwd.nii.gz"
            )
            fusi_scan_path.touch()
            scan_paths_in_session.append(str(fusi_scan_path.relative_to(session_path)))

            # Sidecar JSON file storing task metadata and volume timings.
            tasks_json["awake"]["DelayAfterTrigger"] = round(
                (tasks_json["awake"]["RepetitionTime"] / n_probe_poses)
                * (pose_index - 1),
                2,
            )
            sidecar_json_path = fusi_scan_path.with_suffix("").with_suffix(".json")
            with open(sidecar_json_path, "w") as sidecar_json_file:
                sidecar_json_file.write(json.dumps(tasks_json["awake"], indent=2))

        # Scans TSV file.
        scans_table_path = (
            session_path / f"sub-{subject_index:02d}_ses-{session}_scans.tsv"
        )
        scan_dates = np.array(
            [
                datetime.datetime(2024, 1, 1)
                + datetime.timedelta(
                    days=int(rng.integers(0, 360)),
                    seconds=int(rng.integers(0, 60)),
                    minutes=int(rng.integers(0, 60)),
                    hours=int(rng.integers(0, 24)),
                )
                for _ in range(len(scan_paths_in_session))
            ]
        )
        session_dates.append(scan_dates.min())
        scans_table = pd.DataFrame(
            {
                "filename": scan_paths_in_session,
                "acq_time": [
                    date.strftime("%Y-%m-%dT:%H:%M:%S") for date in scan_dates
                ],
            }
        )
        scans_table.to_csv(scans_table_path, sep="\t")

    session_table_path = subject_path / f"sub-{subject_index:02d}_sessions.tsv"
    session_table = pd.DataFrame(
        {
            "session_id": [f"ses-{session}" for session in sessions],
            "acq_time": [date.strftime("%Y-%m-%dT:%H:%M:%S") for date in session_dates],
        }
    )
    session_table.to_csv(session_table_path, sep="\t")
