#!/usr/bin/env bash
# 并发安全的 data/ 推送：rebase 冲突时对本方数据文件取 theirs 并重试。
set -euo pipefail

MSG="${1:?commit message required}"
shift

if [[ $# -eq 0 ]]; then
  echo "usage: git_push_data.sh <message> <path>..." >&2
  exit 2
fi

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

git add "$@"
if git diff --staged --quiet; then
  echo "No data changes."
  exit 0
fi

git commit -m "$MSG"

resolve_rebase_conflicts() {
  local f
  mapfile -t conflicts < <(git diff --name-only --diff-filter=U 2>/dev/null || true)
  if [[ ${#conflicts[@]} -eq 0 ]]; then
    return 1
  fi
  for f in "${conflicts[@]}"; do
    # rebase 中 theirs = 正在 replay 的本方提交
    git checkout --theirs -- "$f"
    git add -- "$f"
  done
  GIT_EDITOR=true git rebase --continue
}

for attempt in 1 2 3 4 5 6; do
  if git pull --rebase origin master; then
    if git push origin HEAD:master; then
      echo "Pushed on attempt ${attempt}."
      exit 0
    fi
    echo "Push rejected on attempt ${attempt}, retrying..."
  else
    echo "Rebase conflict on attempt ${attempt}, resolving..."
    if ! resolve_rebase_conflicts; then
      git rebase --abort 2>/dev/null || true
    fi
  fi
  sleep $((attempt * 2))
done

echo "Failed to push after retries." >&2
exit 1
