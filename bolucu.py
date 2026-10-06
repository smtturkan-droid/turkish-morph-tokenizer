"""Turkce kok-ek isaretleyici (tokenizer v1'in calisma ani parcasi; yalnizca 'regex' gerekir).

Metindeki her Turkce kelimeye, tablodaki kesim yerlerine gorunmez ISARET (U+E000) koyar:
    "Ben okula gittim"  ->  "Ben okula gittim"
v1 tokenizer'i isaretten boler ve isareti SILER; boylece model okul·a, git·tim gorur, cozulen (decode) metinde isaret olmaz.
Isaretsiz metin (Ingilizce, kod) Qwen3.5 ile birebir ayni token'lara ayrilir.

    from bolucu import Bolucu
    b = Bolucu()                      # varsayilan tablo: bu klasordeki tokenizer/bolunme.tsv
    ids = tok(b.isaretle(metin))["input_ids"]
"""
from pathlib import Path

import regex

ISARET = ""
KELIME = regex.compile(r"[\p{L}\p{M}]+")
_D = Path(__file__).resolve().parent
TABLO = _D / "bolunme.tsv" if (_D / "bolunme.tsv").exists() else _D / "tokenizer" / "bolunme.tsv"


def kucuk(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


class Bolucu:
    """tablo: kelime -> kesimler (bos = bolme; Ingilizce/belirsiz kelimeler bilerek bos).
    Tabloda olmayan kelime icin yedek: bilinen kok + bilinen ek zinciri (en uzun kok), zincirin kendi ic kesimleriyle."""

    def __init__(self, tablo=TABLO):
        self.tablo, self.kokler, self.zincir = {}, set(), {}
        bolum = None
        with open(tablo, encoding="utf-8") as f:
            for satir in f:
                satir = satir.rstrip("\n")
                if satir.startswith("#"):
                    bolum = satir[1:]
                    continue
                k, _, kes = satir.partition("\t")
                kes = tuple(int(x) for x in kes.split(",")) if kes else ()
                if bolum == "kok":
                    self.kokler.add(k)
                elif bolum == "zincir":
                    self.zincir[k] = kes
                else:
                    self.tablo[k] = kes

    def kesimler(self, kelime):
        k = kucuk(kelime)
        if len(k) != len(kelime):
            return ()
        if k in self.tablo:
            return self.tablo[k]
        for i in range(len(k) - 2, 1, -1):                     # yedek: en uzun bilinen kok + bilinen zincir
            if k[:i] in self.kokler and k[i:] in self.zincir:
                return (i,) + tuple(i + x for x in self.zincir[k[i:]])
        return ()

    def _kelime(self, m):
        w = m.group()
        kes = self.kesimler(w)
        if not kes:
            return w
        parca, onceki = [], 0
        for k in kes:
            parca.append(w[onceki:k])
            onceki = k
        parca.append(w[onceki:])
        return ISARET.join(parca)

    def isaretle(self, metin):
        return KELIME.sub(self._kelime, metin.replace(ISARET, ""))
