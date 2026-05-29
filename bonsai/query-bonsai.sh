#!/usr/bin/env bash
set -e

url="${1:-http://127.0.0.1:8080}"
prompt="${2:-What is the capital of France?}"
tokens="${3:-50}"
temp="${4:-0.7}"

curl -s "$url/v1/completions" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"$prompt\", \"n_predict\": $tokens, \"temperature\": $temp}" |
python3 -c "
import json, sys
d = json.load(sys.stdin)
if 'choices' in d:
    print(d['choices'][0]['text'])
    p = d.get('usage', {})
    t = d.get('timings', {})
    print(f\"  [{p.get('completion_tokens',0)} gen / {p.get('prompt_tokens',0)} prompt tokens | {t.get('predicted_per_second',0):.1f} t/s]\")
else:
    print(json.dumps(d, indent=2))
"
