"""HF vs OpenVINO parity check, with ignore_merges=False and True.

Per openvino_tokenizers#780: HF BPE with ignore_merges=True matches OpenVINO's BPE by design.
Needs: transformers, openvino, openvino-tokenizers. Sentences: Tatoeba en-tr (pass the folder as argv[1]).
    python ov_parity.py path/to/tatoeba_en_tr
"""
import json
import sys
import tempfile
from pathlib import Path
YAYIN = Path(__file__).resolve().parent
sys.path.insert(0, str(YAYIN))
import openvino as ov
from openvino_tokenizers import convert_tokenizer
from transformers import PreTrainedTokenizerFast
from bolucu import Bolucu
b = Bolucu(str(YAYIN / "bolunme.tsv"))
t = json.loads((YAYIN / "tokenizer.json").read_text(encoding="utf-8"))
hf = {}
for deger in (False, True):
    t["model"]["ignore_merges"] = deger
    p = Path(tempfile.mkdtemp()) / "tokenizer.json"
    p.write_text(json.dumps(t, ensure_ascii=False), encoding="utf-8")
    hf[deger] = PreTrainedTokenizerFast(tokenizer_file=str(p))
c = ov.Core()
ov_tok = {d: c.compile_model(convert_tokenizer(hf[d]), "CPU") for d in (False, True)}
kok = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("tatoeba_en_tr")
tr = (kok / "Tatoeba.en-tr.tr").read_text(encoding="utf-8").splitlines()[:3000]
en = (kok / "Tatoeba.en-tr.en").read_text(encoding="utf-8").splitlines()[:1000]
for ad, S, isr in (("TR (morph-marked)", tr, True), ("EN", en, False)):
    say = {False: 0, True: 0}; esit = {False: 0, True: 0}; ov_esit = {False: 0, True: 0}; fark = 0; ornek = []
    for s in S:
        m = b.isaretle(s) if isr else s
        h = {d: hf[d](m, add_special_tokens=False)["input_ids"] for d in (False, True)}
        for d in (False, True):
            say[d] += len(h[d])
            ov_esit[d] += ov_tok[d]([m])["input_ids"][0].tolist() == h[d]
            esit[d] += hf[d].decode(h[d]) == s
        if h[False] != h[True]:
            fark += 1
            if len(ornek) < 3:
                ornek.append((s, hf[False].convert_ids_to_tokens(h[False]), hf[True].convert_ids_to_tokens(h[True])))
    print(f"{ad}: HF(F)≠HF(T) {fark}/{len(S)} | OV=HF  F:{ov_esit[False]} T:{ov_esit[True]} /{len(S)} | "
          f"token F:{say[False]} T:{say[True]} ({100 * (say[True] - say[False]) / say[False]:+.2f}%) | round-trip F:{esit[False]} T:{esit[True]}")
    for o in ornek:
        print("   ", o[0][:50], "|", " ".join(o[1])[:90], "→", " ".join(o[2])[:90])
