# Day 1 for a data scientist

1. You do not get to pick a VM. You use the Data Scientist CPU policy. It forces an ML runtime, a small CPU node, single node, 20-minute auto-termination, and the project tags. If the policy rejects your cluster, the policy is right.
2. Read and write under `sandbox` or `dev`. `prod` is not your scratch space. A table without an owner and a comment does not get promoted.
3. Models go to Unity Catalog, not the workspace model registry. Aliases are `@challenger` and `@champion`. You do not move your own model to champion. The promotion job does, and only if the metric beats the current champion and `approved_by` is set.
4. GPU access is a request, not a toggle. Read `docs/runbooks/enable-gpu-compute.md`. Default answer is Foundation Model APIs or CPU. AI Runtime (serverless GPU) is the next answer. A classic GPU VM is the last answer, and this subscription does not have the quota.
5. Etiquette: one GPU node, 15-minute auto-termination, no idle notebook left attached. A GPU node left up overnight is an incident, not a preference.
6. Your training code takes `device`. Ship it as `cpu`. Someone else flips it to `cuda` after quota or AI Runtime is actually available. Do not log "trained on GPU" because the parameter exists.
