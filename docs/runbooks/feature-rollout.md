# Runbook: workspace feature rollout

1. Read the current docs page the same day. Names change. Record the URL and the date in the ADR or the learning log.
2. Check the region table and the Designated Services geo table before you enable anything that processes data.
3. Leave cross-geo processing off unless the geo table says the feature is unavailable in the United States and a named approver accepts the data flow.
4. Capture before and after with the API. `evidence/workspace-conf.json` is the pattern. A screenshot with no timestamp is not evidence.
5. Roll out to the lab workspace first. This lab is the lab. There is no production here, and you should not talk as if there is.
