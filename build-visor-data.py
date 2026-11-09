import json, re, colorsys, datetime
from collections import defaultdict, Counter
from PIL import Image

import os
BASE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(BASE, "thumbs")

tr = json.load(open(f"{BASE}/transcripciones-tallas.json"))
cat = json.load(open(f"{BASE}/catalogo-agrupado.json"))["products"]
by_id = {str(p["id"]): p for p in cat}

byp = defaultdict(list)
for r in tr["tables"]:
    byp[r["product_id"]].append(r)

CANON = ("pecho", "manga", "talle", "ruedo_o_cadera")

def to_num(v):
    if isinstance(v, int):
        return v, False
    if isinstance(v, str):
        m = re.findall(r"\d+", v)
        if len(m) == 2:
            return max(int(m[0]), int(m[1])), True
        if len(m) == 1:
            return int(m[0]), False
    return None, True

def dominant_color(pid):
    path = os.path.join(TMP, f"{pid}.jpg")
    try:
        im = Image.open(path).convert("RGB")
    except Exception:
        return None
    w, h = im.size
    px = im.load()
    bins = Counter()
    samples = []
    for y in range(int(h*0.28), int(h*0.72), 3):
        for x in range(int(w*0.28), int(w*0.72), 3):
            r, g, b = px[x, y]
            hh, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            if s < 0.22 or v < 0.15:
                continue
            hb = int((hh*360) // 20) * 20
            bins[hb] += 1
            samples.append((hb, r, g, b, s))
    if not samples or len(samples) < 60:
        return None
    top = bins.most_common(1)[0][0]
    sel = [s for s in samples if s[0] == top]
    r = sum(s[1] for s in sel)//len(sel)
    g = sum(s[2] for s in sel)//len(sel)
    b = sum(s[3] for s in sel)//len(sel)
    return "#%02x%02x%02x" % (r, g, b)

products = []
skipped = []

for pid, guides in byp.items():
    p = by_id.get(pid)
    if not p:
        continue
    best = None
    for r in guides:
        d = {m["canonical"]: m for m in r["measures"]}
        if not all(k in d for k in CANON):
            continue
        n = len(r["sizes"])
        vals, approx, good = {}, False, True
        for k in CANON:
            vv = []
            for x in d[k]["values"]:
                x2, a = to_num(x)
                if x2 is None:
                    good = False
                    break
                vv.append(x2)
                approx = approx or a
            if not good or len(vv) != n:
                good = False
                break
            vals[k] = vv
        if good:
            cand = (r, vals, approx)
            if best is None or len(r["sizes"]) > len(best[0]["sizes"]):
                best = cand

    if not best:
        skipped.append(p["title"])
        continue

    r, vals, approx = best
    sizes = [{"id": s, "chest": vals["pecho"][i], "sleeve": vals["manga"][i],
              "talle": vals["talle"][i], "hem": vals["ruedo_o_cadera"][i]} for i, s in enumerate(r["sizes"])]

    color = dominant_color(pid)
    is_hero = p["handle"] == "cortaviento-purple-spring-trend"
    base = "M" if any(s["id"] == "M" for s in sizes) else sizes[len(sizes)//2]["id"]

    products.append({
        "sku": p["handle"],
        "title": p["title"],
        "type": p["type"],
        "base": base,
        "color": color,
        "palette": "hero" if is_hero else "neutral",
        "ease": 30 if is_hero else 16,
        "approx": approx,
        "sizes": sizes,
        "source": r["image"],
    })

products.sort(key=lambda x: x["title"].lower())

out = {
    "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
    "note": "Tablas normalizadas a 4 puntos (pecho, manga, talle, ruedo). Fuente: guías transcritas desde las descripciones de producto.",
    "count": len(products),
    "products": products,
}
json.dump(out, open(f"{BASE}/visor-data.json", "w"), ensure_ascii=False, indent=1)

print("productos:", len(products), "| omitidos:", len(skipped))
print("con color detectado:", sum(1 for p in products if p["color"]))
print("aprox (rangos):", sum(1 for p in products if p["approx"]))
print("\nmuestra:")
for p in products[:6]:
    print(" ", p["sku"], "|", p["color"], "|", [(s["id"], s["chest"]) for s in p["sizes"]])
print("\nomitidos:", skipped)
