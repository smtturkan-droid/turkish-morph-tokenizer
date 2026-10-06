---
license: apache-2.0
language:
- tr
- en
tags:
- tokenizer
- turkish
- morphology
- qwen3.5
- openvino
base_model: Qwen/Qwen3.5-2B
---

# Turkish Morphology-Aware Tokenizer for Qwen3.5 (v1)

A drop-in extension of the **Qwen3.5** tokenizer that splits Turkish words at **root + suffix boundaries** instead of arbitrary byte-pair fragments, and makes Turkish nearly as cheap as English in tokens. **English and code tokenization is unchanged** (Qwen's original tokens and merges are kept as-is).

**Hugging Face:** https://huggingface.co/smtturkan/turkish-morph-tokenizer · **GitHub:** https://github.com/smtturkan-droid/turkish-morph-tokenizer

> Türkçe özet: Qwen3.5 tokenizer'ına 32 bin Türkçe kök/ek parçası eklendi. Kelimeler kökünden ve ekinden bölünüyor (okul·a, git·tim). Kökü bütün tutma %56'dan %92'ye çıktı, Türkçe metnin token maliyeti İngilizcenin 1,28 katından 1,07 katına indi. İngilizce ve kod aynı kalıyor.

## Results

Measured on the **test** splits of the UD Turkish treebanks (gold morphological segmentation, never used for building):

| | BOUN root intact | BOUN exact boundaries | IMST root intact | IMST exact boundaries | tokens / word |
|---|---|---|---|---|---|
| Qwen3.5 (original) | 56.3% | 44.4% | 56.0% | 43.7% | 2.08 |
| **This tokenizer** | **91.7%** | **90.2%** | **92.3%** | **90.8%** | **1.62** |

- Root intact **or** split only at valid suffix boundaries (e.g. `temiz·lik`): **96.3% / 96.5%**
- Turkish/English token ratio on parallel Tatoeba sentences: **1.28× → 1.07×**
- Round trip `decode(encode(text)) == text`: **100%**
- English sentences tokenized identically to Qwen3.5: **99.6%**
- **OpenVINO parity:** the converted OpenVINO tokenizer produces identical ids to HF on 4000/4000 test sentences (3000 Turkish, 1000 English)

Details: [`OLCUM.md`](OLCUM.md) (Turkish).

## How it works

1. `bolucu.py` inserts an invisible marker (U+E000) at morpheme boundaries of Turkish words, using a lookup table (`bolunme.tsv`) with a root + suffix-chain fallback for unseen words.
2. The tokenizer's pre-tokenizer splits on the marker and **removes** it, so the model sees `okul·a`, `git·tim`, while decoded text never contains the marker.
3. New tokens start at id 248320; the first 243 fill Qwen's unused embedding rows. Qwen's own tokens and merges are untouched, so text without markers (English, code) tokenizes exactly as in Qwen3.5.

```python
from transformers import PreTrainedTokenizerFast
from bolucu import Bolucu            # needs: pip install regex

tok = PreTrainedTokenizerFast(tokenizer_file="tokenizer.json")
b = Bolucu()                          # loads bolunme.tsv next to bolucu.py
ids = tok(b.isaretle("Evlerimizden çıktık."))["input_ids"]
print(tok.convert_ids_to_tokens(ids))
print(tok.decode(ids))                # original text, no marker
```

**Note:** the new token embeddings are **not trained**. To benefit in a model, resize the embeddings of Qwen3.5 and continue pre-training on Turkish text. This release is the tokenizer only.

## OpenVINO note

Extending a BPE vocabulary above Qwen's added tokens triggers a crash in `openvino_tokenizers` when the vocab has an id gap ([openvinotoolkit/openvino_tokenizers#780](https://github.com/openvinotoolkit/openvino_tokenizers/issues/780)). This tokenizer avoids it by also writing the special tokens into `model.vocab` with their own ids, so it converts cleanly with `convert_tokenizer`.

## Data used to build it

Only sources that allow redistribution of derived work were used:

| Source | License |
|---|---|
| Qwen3.5 tokenizer (base vocabulary & merges) | Apache-2.0 |
| Turkish Wikipedia (2023-11-01 dump) | CC BY-SA 4.0 |
| Wikisource, Wikibooks, Wikiquote (Turkish) | CC BY-SA 4.0 |
| Grand National Assembly of Turkey (TBMM) plenary records 2002–2026 | public official records |
| Tatoeba Turkish–English | CC BY 2.0 FR |
| Aya dataset (Turkish part) | Apache-2.0 |
| UD Turkish BOUN treebank (train split, gold segmentation) | CC BY-SA 4.0 |
| Zemberek-NLP morphological analyzer | Apache-2.0 |

The UD Turkish IMST treebank (CC BY-NC-SA) was used **only for evaluation** (test split), not for building.

## License

Apache-2.0 (same as the Qwen3.5 tokenizer it extends). Please also respect the attribution terms of the data sources above.
