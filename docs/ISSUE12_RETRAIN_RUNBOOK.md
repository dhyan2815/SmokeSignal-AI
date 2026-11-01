# Issue #12 runbook: data layer fixes and retrain

Branch: `feat/12-multiclass-false-positive-reduction`. Everything below is reproducible from the repo plus the Kaggle wildfire dataset.

## Why run 1 failed (evidence)

| Finding | Evidence | Fix |
|---|---|---|
| Fire recall fell 96.8% -> 85.6% | Binary model re-run through the same generator pipeline reproduces 96.09% / 96.81%, so the pipeline is fine and the drop is real | Stage-2 lr 1e-5 -> 1e-4, 20 epochs, milder jitter (hue +-8 deg, sat/val 0.8-1.2) |
| Smoke labels noisy | 31% of synthetic `smoke` images differed from their `clear` source by < 10 grey levels | Plume must cover 15-70% of the tile and change it by >= 15 levels; now 0% below 10 |
| Model learned generator fingerprints | New hold-out families (never trained on): cumulus-cloud FPR 77.8%, valley-fog FPR 85.2%, plume smoke recall 31.2%, vs 0.2% / 2.4% / 87.8% on the trained families | Hold-out families are test-only; they are the generalization gate |
| No real-world evidence | Everything new was synthetic | `data/real_eval/` (real images, never trained on) + validated ingest pipeline |
| Original dataset | 42,850 files, 1 hash spans two splits, 0 conflicting labels | No change needed |

Run-1 model on real IGNIS images: smoke alert-rate 65.9%, fire alert-rate 52.6% (n=229 / 19).

## Data layer

- `src/synth.py`: generators. Trained families: sunset, cloud, fog, smoke. Hold-out (test only): cloud_cumulus, fog_valley, smoke_plume.
- `src/curate_dataset.py`: builds `data/multiclass/` (hardlinks, gitignored) + `manifest.csv`.
- `src/ingest_external.py`: ingests real images into `data/real_eval/` with a manifest row per image (source, URL, licence, tier open|research, dHash), centre-crop to 350 px, dedup (dHash hamming <= 4) against all 42,850 existing tiles and within the source.
- Ingested so far: IGNIS (CC BY 4.0, open tier): 229 smoke + 19 fire (13 near-duplicates dropped, 0 clashes with existing tiles).
- Pending sources (not downloaded; need sizes/licences confirmed): Boreal Forest Fire UAV (CC BY 4.0), HPWREN smoke (CC BY-NC-SA, research tier), CloudSEN12+ subset (CC0), sunset photos (Wikimedia Commons / WordPress CC0).

## Commands

```bash
# 1. dataset (reruns clean; ~5 min)
python src/curate_dataset.py --src "<kaggle wildfire dataset root>"
# 2. real images
python src/ingest_external.py --name ignis --src data/raw_external/ignis/data --yolo-map 3=fire,1=smoke,2=smoke \
    --license CC-BY-4.0 --tier open --url https://huggingface.co/datasets/matjs/ignis --existing-src "<kaggle root>"
# 3. retrain (two stages, up to ~25 epochs)
python src/train_multiclass.py
# 4. evaluate (gates)
python src/evaluate_multiclass.py
```

## Gates (evaluate_multiclass.py)

1. Binary precision and recall on ORIGINAL test tiles within 2 points of 96.09% / 96.81%.
2. FPR < 5% on synthetic sunset / cloud / fog, **including the hold-out families**.
3. Reported, not yet gated: smoke / plume recall, and the real-image alert-rates (`data/real_eval`).

## Known limits

- Synthetic data is an approximation; real cloud / fog / sunset satellite images are still missing (only 248 real images, smoke/fire).
- The backbone is small (64x64 input). If recall is still short after this run, widen the CNN before touching data again.
- Ground-level sources must supply both fire and non-fire from the same domain, or "ground photo" becomes a shortcut for "not fire".
