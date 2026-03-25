Overlay layer for repo-specific customizations.

Anything placed here is considered source-of-truth for the consuming repo.

Rules:
- overlay files override stack/base on apply-overlay
- preserve_files prevents overwrite during update-stack
- copy_files reapplies overlay after stack sync
