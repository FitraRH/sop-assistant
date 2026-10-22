"""Run eval/questions.json and eval/holdout.json, write eval/results.md."""
import json
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sop_assistant.answer import Assistant  # noqa: E402

mark = lambda v: "-" if v is None else ("✅" if v else "❌")


def run(bot: Assistant, q: dict) -> dict:
    a = bot.ask(q["question"])
    expected = {tuple(x) for x in q["expected_sources"]}  # empty = not answerable from the documents
    ret = {(r["doc"], r["section"]) for r in a.retrieved}
    cited = {(c.doc, c.section) for c in a.citations}
    scoped = bool(expected)
    return {**q, "status": a.status, "answer": a.answer, "reason": a.reason, "mode": a.mode,
            "status_ok": a.status in q["expected_status"],
            "retrieved": bool(expected & ret) if scoped else None,
            "cited": bool(expected & cited) if scoped else None,
            "keywords": all(k.lower() in a.answer.lower() for k in q["must_contain"]) if scoped else None}


def summary(rows: list[dict]) -> list[str]:
    scoped = [r for r in rows if r["retrieved"] is not None]
    unscoped = [r for r in rows if r["retrieved"] is None]
    n = lambda key, rs: f"{sum(bool(r[key]) for r in rs)}/{len(rs)}"
    return [f"Status benar: {n('status_ok', rows)}",
            f"Dalam cakupan: bagian benar ditemukan {n('retrieved', scoped)}, dikutip {n('cited', scoped)}, "
            f"fakta kunci lengkap {n('keywords', scoped)}",
            f"Di luar cakupan: ditolak dengan benar {n('status_ok', unscoped)}"]


def main() -> None:
    bot = Assistant()
    cfg = (f"embedding={bot.s.embed_model if bot.s.embed_backend == 'fastembed' else 'hash'}, "
           f"llm={bot.s.llm_model if bot.llm else 'tanpa LLM (ekstraktif)'}")
    sets = {name: json.loads((ROOT / "eval" / f"{name}.json").read_text(encoding="utf-8")) for name in ("questions", "holdout")}
    md, all_rows = [f"# Hasil Evaluasi\n\nKonfigurasi: {cfg}\n"], []
    for name, qs in sets.items():
        rows = []
        for q in qs:
            rows.append(run(bot, q))
            print(f"{q['id']} {rows[-1]['status']:<10} {mark(rows[-1]['status_ok'])}", flush=True)
        all_rows += rows
        md += [f"## Set {name}", *[f"- {line}" for line in summary(rows)], "",
               "| ID | Kategori | Harapan → Hasil | Ditemukan | Dikutip | Fakta |", "|---|---|---|---|---|---|"]
        md += [f"| {r['id']} | {r['category']} | {'/'.join(r['expected_status'])} → {r['status']} {mark(r['status_ok'])} "
               f"| {mark(r['retrieved'])} | {mark(r['cited'])} | {mark(r['keywords'])} |" for r in rows] + [""]
    md += ["## Jawaban lengkap", ""]
    for r in all_rows:
        md += [f"**{r['id']}. {r['question']}** ({r['status']}, {r['mode']})", "", r["answer"].replace("\n", "\n> "), ""]
        md += [f"Catatan: {r['reason']}", ""] if r["reason"] else []
    (ROOT / "eval" / "results.md").write_text("\n".join(md), encoding="utf-8")
    print("\n" + "\n".join(f"{n}: " + " | ".join(summary([r for r in all_rows if r["id"][0] == p]))
                            for n, p in (("questions", "Q"), ("holdout", "H"))))
    print(f"Konfigurasi: {cfg}\nDetail: eval/results.md")


if __name__ == "__main__":
    main()