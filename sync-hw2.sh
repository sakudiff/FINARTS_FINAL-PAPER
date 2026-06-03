#!/bin/bash
# =============================================================================
# sync-hw2.sh — Monitor hw2.pdf for changes and mirror to Google Drive
# =============================================================================
# Watches for LaTeX recompilation of hw2.pdf and copies the new render to
# the Google Drive folder automatically.
#
# Started automatically from ~/.zshrc (must run as child of a GUI process
# like Terminal on macOS for File Provider / TCC access).
# =============================================================================

PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

SRC="/Users/hoshi/Local Code/FINARTS/Assignments/Homework 2/hw2.pdf"
DST="/Users/hoshi/Google Drive/My Drive/DLSU DRIVE [MAIN]/AY 2025-2026/Term 3/[1253_FINARTS_C01] - APPLIED REGRESSION AND TIME SERIES ANALYSIS FOR FINANCIAL RESEARCH/Assignments/Homework 2/hw2.pdf"
LOG="$HOME/Library/Logs/sync-hw2.log"
PIDFILE="/tmp/sync-hw2.pid"

# --- PID file management (prevent duplicates) ---
if [ -f "$PIDFILE" ]; then
    OLD_PID=$(cat "$PIDFILE" 2>/dev/null)
    if kill -0 "$OLD_PID" 2>/dev/null; then
        exit 0  # Already running
    fi
fi
echo $$ > "$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT HUP INT TERM QUIT

# --- Ensure destination exists ---
DST_DIR="$(dirname "$DST")"
if [ ! -d "$DST_DIR" ]; then
    echo "[$(date)] ERROR: Destination directory not found: $DST_DIR" >> "$LOG"
    exit 1
fi

echo "[$(date)] sync-hw2.sh started (PID $$). Watching: $SRC" >> "$LOG"

# --- Watcher loop ---
# fswatch -o: one integer per batch of events (debounced).
# --event=Updated + AttributeModified catches writes from latexmk, xelatex, etc.
fswatch -o --event=Updated --event=AttributeModified "$SRC" 2>>"$LOG" | while read -r _; do
    # Debounce: wait for multi-pass LaTeX writes to finish
    sleep 2

    if [ -f "$SRC" ]; then
        cp "$SRC" "$DST" && \
            echo "[$(date)] Synced to Google Drive" >> "$LOG"
    fi
done
