# GPU CI design (not provisioned)

This greeting CLI does not use a GPU. Adding CUDA to its release gate would test unrelated
infrastructure and add a supply-chain dependency. The following design applies if a future
CLI gains a real GPU backend; no GPU execution is claimed for the submitted CLI.

## Workload and triggers

Per release: after CPU lint, source checks and clean artifact installation pass, rent one
ephemeral Runpod RTX 4090 Pod. Install the exact release wheel and a separately hash-locked
CUDA test stack. Verify GPU detection, one known-answer computation against a CPU reference,
numerical tolerance, and actual backend selection (CPU fallback must fail). Include warmup
and bounded startup time. Record CUDA/driver/device versions, image digest and artifact SHA256.
Budget 15 minutes including provisioning, downloads, execution and cleanup.

Nightly: trusted default-branch schedule, one 30-minute job including provisioning. Run larger
fixtures, memory pressure and repeated results, compare performance only after warmup with
a tolerance appropriate for shared infrastructure. Distinguish infrastructure failures from
numerical failures. A release failure blocks GPU-enabled release; a nightly failure creates
an actionable investigation and disables the next automatic release until triaged.

## Monthly cost model

Assumptions: 30 nightlies x 0.5 hours + 4 releases x 0.25 hours = 16 GPU hours.
Runpod's live pricing page, checked 2026-11-10 (page updated November 4), lists RTX 4090
at $0.89/hour: compute $14.24/month. Reserve 25% retry/startup headroom: $17.80 compute.
An optional 20 GB standard network volume at $0.07/GB-month adds $1.40, giving $19.20.
Request a $25/month operational cap; taxes, region/availability changes, network transfer and
other storage charges are not included. Recheck the actual deployment quote before spending.
These are workload assumptions, not measured execution times. No instance has been rented.

Source: https://www.runpod.io/pricing

## Prevent waste and credential exposure

- CPU gates run before provisioning; no fork PR or arbitrary PR code reaches a paid runner.
- A trusted controller provisions one ephemeral runner for one run, with no PyPI or repository
  write credentials on it. Keep the provider credential in the controller only.
- Pin the CUDA image digest, wheel hash, datasets and Python dependencies. Bound downloads.
- Concurrency one; cancel superseded nightlies, and keep release evidence. No automatic retries
  for deterministic test failures; allow at most one infrastructure retry within budget.
- Controller cleanup runs even after cancellation. An independent reaper terminates Pods past
  a 45-minute lease, covering controller death. Persist only reports outside the Pod.
- Terminate, rather than merely stop, disposable Pods. Stop retains billable storage.
- Track provisioned Pod IDs, elapsed billed time and daily spend. The controller refuses new
  work once its monthly allowance is exhausted; a billing alert alone is not a hard cap.

Lifecycle reference: https://docs.runpod.io/pods/manage-pods
