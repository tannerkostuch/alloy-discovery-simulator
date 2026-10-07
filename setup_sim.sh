#!/usr/bin/env bash
# setup_sim.sh — builds the simulation environment in ./.venv. No sudo, nothing system-wide: everything goes into .venv,
# plus uv itself (a Python installer) into ~/.local/bin if it is not on the PATH yet — that step downloads and runs
# uv's installer from astral.sh; install uv yourself first if you would rather not. Re-runnable.
# Log: logs/setup.log, summary: ENV_REPORT.txt
#   1. uv → a private CPython 3.12
#   2. PyTorch — the CPU wheel by default (every result in this repository was computed on the CPU). Another wheel:
#        TORCH_INDEX=rocm7.0 bash setup_sim.sh     any index name under download.pytorch.org/whl/ (rocm… AMD, cu… NVIDIA)
#      a wheel that does not import falls back to the CPU one. Check a GPU's forces before trusting it (diag_cantor.py).
#   3. mace-torch, ase, pymatgen, matminer, scipy, pandas, spglib, tabulate
#   4. the MACE-MPA-0 model (downloaded once into ~/.cache/mace)
#   5. a GPU probe: does torch see a card?
set -u
SIM="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
mkdir -p "$SIM/logs" "$SIM/cache" "$SIM/results" "$SIM/data"
LOG="$SIM/logs/setup.log"
REP="$SIM/ENV_REPORT.txt"
export PATH="$HOME/.local/bin:$PATH"
TORCH_INDEX="${TORCH_INDEX:-cpu}"
{
echo "== $(date '+%F %T') setup (torch index: $TORCH_INDEX)"
# 1. uv + python 3.12
if ! command -v uv >/dev/null 2>&1; then
  echo "-- installing uv"; curl -LsSf https://astral.sh/uv/install.sh | sh 2>&1 | tail -2
fi
UV="$(command -v uv)"
if [ -z "$UV" ]; then echo "!! uv is not available — install it (https://docs.astral.sh/uv/) or use: pip install -r requirements.txt"; exit 1; fi
"$UV" --version
"$UV" python install 3.12 2>&1 | tail -2
[ -x "$SIM/.venv/bin/python" ] || "$UV" venv --python 3.12 "$SIM/.venv" 2>&1 | tail -2
PY="$SIM/.venv/bin/python"
echo "-- python: $("$PY" --version)"
# 2. torch
torch_ok() { "$PY" -c "import torch" >/dev/null 2>&1; }
if ! torch_ok; then
  echo "-- installing PyTorch from download.pytorch.org/whl/$TORCH_INDEX"
  "$UV" pip install --python "$PY" torch --index-url "https://download.pytorch.org/whl/$TORCH_INDEX" 2>&1 | tail -3
  if ! torch_ok && [ "$TORCH_INDEX" != "cpu" ]; then
    echo "-- that wheel did not import; CPU-only PyTorch instead"
    "$UV" pip uninstall --python "$PY" torch >/dev/null 2>&1
    "$UV" pip install --python "$PY" torch --index-url https://download.pytorch.org/whl/cpu 2>&1 | tail -3
  fi
  torch_ok || echo "-- no PyTorch from download.pytorch.org — the default wheel from PyPI comes with the rest (larger: it carries the CUDA libraries)"
fi
# 3. the rest (and PyTorch from PyPI, if step 2 did not get one)
"$UV" pip install --python "$PY" -r "$SIM/requirements.txt" 2>&1 | tail -3
echo "-- torch: $("$PY" -c "import torch; print(torch.__version__)" 2>&1 | tail -1)"
"$PY" - <<'PYEOF' 2>&1
import importlib
for m in ("torch", "mace", "ase", "pymatgen", "matminer", "scipy", "pandas", "spglib", "e3nn", "tabulate"):
    try:
        mod = importlib.import_module(m); print(f"   {m:10s} {getattr(mod, '__version__', 'ok')}")
    except Exception as e:
        print(f"   {m:10s} MISSING ({e})")
PYEOF
# 4. the MACE model (download only)
echo "-- MACE-MPA-0 model:"
timeout 900 "$PY" -c "
from mace.calculators import mace_mp
c = mace_mp(model='medium-mpa-0', device='cpu', default_dtype='float64'); print('   model loaded on cpu')
" 2>&1 | grep -v "^$" | tail -1
# 5. the GPU
echo "-- GPU probe:"
"$PY" - <<'PYEOF' 2>&1 | sed 's/^/   /'
import torch, time
ok = torch.cuda.is_available()
print("torch.cuda.is_available():", ok)
if ok:
    print("device:", torch.cuda.get_device_name(0))
    a = torch.randn(2048, 2048, device="cuda"); torch.cuda.synchronize(); t = time.time()
    for _ in range(10): b = a @ a
    torch.cuda.synchronize(); print(f"matmul 2048² x10: {time.time()-t:.2f} s on the GPU")
    print("The runs still use the CPU unless you pass --device cuda; run diag_cantor.py first — it compares the GPU's forces with the CPU's.")
else:
    print("no GPU seen by torch — everything runs on the CPU, which is what the results in this repository used.")
PYEOF
echo "== done $(date '+%F %T')"
} 2>&1 | tee -a "$LOG" > "$REP"
cat "$REP"
