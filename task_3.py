import timeit
from typing import Callable, List, Dict, Any


def boyer_moore(text: str, pattern: str) -> int:
    pattern_length = len(pattern)
    text_length = len(text)
    if pattern_length == 0:
        return 0
    skip_table = {}
    for idx in range(pattern_length - 1):
        skip_table[pattern[idx]] = pattern_length - idx - 1
    text_idx = pattern_length - 1
    while text_idx < text_length:
        pattern_idx = pattern_length - 1
        scan_idx = text_idx
        while pattern_idx >= 0 and text[scan_idx] == pattern[pattern_idx]:
            scan_idx -= 1
            pattern_idx -= 1
        if pattern_idx == -1:
            return scan_idx + 1
        text_idx += skip_table.get(text[text_idx], pattern_length)
    return -1


def kmp_search(text: str, pattern: str) -> int:
    text_length = len(text)
    pattern_length = len(pattern)
    if pattern_length == 0:
        return 0
    lps = [0] * pattern_length
    length = 0
    i = 1
    # Preprocess the pattern (calculate lps[] array)
    while i < pattern_length:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    text_idx = 0
    pattern_idx = 0
    # Search for the pattern in the text
    while text_idx < text_length:
        if pattern[pattern_idx] == text[text_idx]:
            text_idx += 1
            pattern_idx += 1
        if pattern_idx == pattern_length:
            return text_idx - pattern_idx
        elif text_idx < text_length and pattern[pattern_idx] != text[text_idx]:
            if pattern_idx != 0:
                pattern_idx = lps[pattern_idx - 1]
            else:
                text_idx += 1
    return -1


def rabin_karp(text: str, pattern: str) -> int:
    text_length = len(text)
    pattern_length = len(pattern)
    if pattern_length == 0:
        return 0
    d = 256
    q = 101
    h = pow(d, pattern_length - 1) % q
    pattern_hash = 0
    window_hash = 0
    # Calculate the hash value of pattern and first window of text
    for i in range(pattern_length):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        window_hash = (d * window_hash + ord(text[i])) % q
    # Slide the pattern over text one by one
    for s in range(text_length - pattern_length + 1):
        if pattern_hash == window_hash:
            if text[s:s + pattern_length] == pattern:
                return s
        if s < text_length - pattern_length:
            window_hash = (
                d * (window_hash - ord(text[s]) * h) + ord(text[s + pattern_length])) % q
            if window_hash < 0:
                window_hash += q
    return -1


def measure_time(
        search_func: Callable[[str, str], int], text: str, pattern: str) -> float:
    return timeit.timeit(lambda: search_func(text, pattern), number=10)


def main():
    # Load texts
    with open('стаття_1.txt', encoding='utf-8') as file:
        article_1_text = file.read()
    with open('стаття_2.txt', encoding='utf-8') as file:
        article_2_text = file.read()

    # Choose substrings for search
    existing_substring_1 = article_1_text[50:70] if len(
        article_1_text) > 70 else article_1_text[:20]
    nonexistent_substring_1 = "qwertyuiopasdfghjklz"

    existing_substring_2 = article_2_text[100:120] if len(
        article_2_text) > 120 else article_2_text[:20]
    nonexistent_substring_2 = "zxcvbnmasdfghjklqwer"

    results: List[Dict[str, object]] = []

    # Measure execution time for each algorithm and pattern
    for article_name, article_text, existing_substring, nonexistent_substring in [
        ("стаття_1", article_1_text, existing_substring_1, nonexistent_substring_1),
        ("стаття_2", article_2_text, existing_substring_2, nonexistent_substring_2)
    ]:
        for pattern, pattern_type in [
                (existing_substring, "існуючий"), (nonexistent_substring, "вигаданий")]:
            bm_time = measure_time(boyer_moore, article_text, pattern)
            kmp_time = measure_time(kmp_search, article_text, pattern)
            rk_time = measure_time(rabin_karp, article_text, pattern)
            results.append({
                "article": article_name,
                "pattern_type": pattern_type,
                "Boyer-Moore": bm_time,
                "KMP": kmp_time,
                "Rabin-Karp": rk_time
            })

    # Write results to markdown file
    with open("results.md", "w", encoding="utf-8") as md:
        md.write("# Порівняння алгоритмів пошуку підрядка\n\n")
        md.write(
            "| Стаття    | Тип підрядка | Boyer-Moore | KMP      | Rabin-Karp |\n")
        md.write(
            "|-----------|--------------|-------------|----------|------------|\n")
        for r in results:
            md.write(
                f"| {
                    r['article']} | {
                    r['pattern_type']} | {
                    r['Boyer-Moore']:.6f} | {
                    r['KMP']:.6f} | {
                        r['Rabin-Karp']:.6f} |\n")

        md.write("\n**Висновки:**\n")
        for article in ["стаття_1", "стаття_2"]:
            fastest_result: Dict[str, Any] = min(
                (r for r in results if r["article"] == article and r["pattern_type"] == "існуючий"),
                key=lambda x: min(x["Boyer-Moore"], x["KMP"], x["Rabin-Karp"])
            )
            fastest_algo: str = min(
                ["Boyer-Moore", "KMP", "Rabin-Karp"],
                key=lambda algo: float(fastest_result[algo])
            )
            md.write(
                f"- Для {article} (існуючий підрядок) найшвидший алгоритм: **{fastest_algo}**.\n")

        total_times = {
            "Boyer-Moore": sum(r["Boyer-Moore"] for r in results),
            "KMP": sum(r["KMP"] for r in results),
            "Rabin-Karp": sum(r["Rabin-Karp"] for r in results)
        }
        overall_fastest = min(total_times, key=total_times.get)
        md.write(f"- В цілому найшвидший алгоритм: **{overall_fastest}**.\n")


if __name__ == "__main__":
    main()
