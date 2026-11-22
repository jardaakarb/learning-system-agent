"""
Batch Audio Studio for Learning System Agent (V3)
Generates natural conversational audio podcasts in Czech using Google Speech API,
with built-in Humanizer anti-slop editing and per-milestone batching.
"""

import os
import sys
import json
import time
import wave
import base64
import argparse
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_FFMPEG = r"C:\Users\Jaroslav\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-essentials_build\bin\ffmpeg.exe"

def find_ffmpeg():
    if os.path.exists(DEFAULT_FFMPEG):
        return DEFAULT_FFMPEG
    try:
        res = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True, check=True)
        paths = res.stdout.strip().splitlines()
        if paths:
            return paths[0]
    except Exception:
        pass
    return "ffmpeg"

def find_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    candidates = [
        r"C:\Users\Jaroslav\Desktop\myvault_apps\broll-generator\.env",
        r"C:\Users\Jaroslav\Desktop\myvault_apps\learning-system-agent\.env",
        r"c:\Users\Jaroslav\Desktop\myvault_apps\.env"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
            except Exception:
                pass
    return None

def call_gemini_json(prompt: str, api_key: str, model: str = "gemini-2.5-flash") -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)

def humanize_script_turns(turns: list, api_key: str) -> list:
    """
    Applies the Humanizer skill rules (Wikipedia 'Signs of AI writing' adaptation)
    to eliminate chatbot tropes, staged openers, artificial agreements, and forced formulas
    before sending text to audio synthesis.
    """
    # Batch turns in chunks of ~20 to avoid token cutoff while maintaining flow
    chunk_size = 20
    humanized_all = []

    for i in range(0, len(turns), chunk_size):
        chunk = turns[i:i + chunk_size]
        prompt = f"""
Jsi nekompromisní lidský editor podle metodiky Humanizer (odstranění všech stop AI textu a chatbotových manýrů).
Tvým úkolem je přepsat repliky dialogu tak, aby zněly jako dva skuteční zkušení kolegové, kteří spolu mluví naprosto přirozeně, věcně, uvolněně a bez jakýchkoliv klišé.

STRIKTNÍ PRAVIDLA HUMANIZACE:
1. ZÁKAZ ÚVODNÍHO PŘIKYVOVÁNÍ: Žádné "Máš naprostou pravdu, Petře", "Přesně tak, Eleno", "To je skvělý postřeh". Lidé takhle v reálu nemluví – rovnou navaž konkrétní myšlenkou, protiargumentem nebo faktem.
2. ZÁKAZ STAGED OPENERS: Žádné "Pojďme se ponořit do...", "Dnes se podíváme na...", "Upřímně?", "Tady je věc:".
3. ZÁKAZ VZORCE "Není to o X, ale o Y": Vyjádři to přímo jedním věcným sdělením bez umělého kontrastu.
4. ZÁKAZ HLUBOKOMYSLNÝCH FRÁZÍ: Žádné "ve své podstatě", "v dnešním dynamickém světě", "základním stavebním kamenem", "to je ta skutečná výhra".
5. ZÁKAZ NUCENÝCH TROJIC: Žádné "rychlost, efektivita a bezpečnost" – řekni to přirozeně.
6. ZÁKAZ AI SLOV: vyhoď slova jako robustní, klíčový, fascinující, revoluční, krajina/landscape, pivotální.
7. ZÁKAZ SPOJOVACÍCH POMLČEK: Místo dlouhých pomlček použij tečku nebo čárku.
8. PONECH VŠECHNA FAKTA: jména nástrojů, čísla, reálné postupy, chybové stavy a kód neměň!
9. PŘIROZENÁ MLUVENÁ ČEŠTINA: živý jazyk, střídání kratších a delších vět.

Vstupní repliky:
{json.dumps(chunk, ensure_ascii=False, indent=2)}

Vrať POUZE validní JSON pole objektů se strukturou:
[
  {{"speaker": "...", "text": "..."}}
]
"""
        try:
            cleaned_chunk = call_gemini_json(prompt, api_key)
            if isinstance(cleaned_chunk, list):
                for orig_turn, clean_turn in zip(chunk, cleaned_chunk):
                    # Preserve original voice mapping while taking humanized text
                    clean_turn["voice"] = orig_turn.get("voice", "Fenrir" if clean_turn.get("speaker") == "Petr" else "Aoede")
                    humanized_all.append(clean_turn)
            else:
                humanized_all.extend(chunk)
        except Exception as e:
            print(f"    [Humanizer warning: {e}, using original text for chunk {i}]")
            humanized_all.extend(chunk)

    return humanized_all

def build_organic_script_prompt(module_title: str, module_index: int, total_modules: int,
                                previous_lessons_context: str, knowledge_pack_content: str,
                                duration_minutes: int = 12) -> str:
    target_words = int(duration_minutes * 140)
    min_turns = max(16, duration_minutes * 2)

    return f"""
Jsi ostřílený technologický mentor a pedagogický architekt. Píšeš dialogický scénář pro audio podcast v češtině o délce zhruba {duration_minutes} minut (cca {target_words} slov, minimálně {min_turns} replik).

TÉMA TÉTO LEKCE (Modul {module_index}/{total_modules}):
"{module_title}"

ZNALOSTNÍ PODKLADY Z RESEARCH BALÍČKU (Fakta, čísla, pasti, mechanismy):
{knowledge_pack_content[:15000]}

PŘEDCHOZÍ LEKCE A KONTINUITA (CO UŽ BYLO PROBRÁNO):
{previous_lessons_context if previous_lessons_context else "Toto je první úvodní lekce kurzu."}

POKYNY PRO DIALOG (PŘIROZENÝ OBSAH, ŽÁDNÁ UMĚLÁ STRUKTURA):
1. ŽÁDNÉ FORMÁLNÍ DĚLENÍ NA AKTY: Neškatulkuj dialog do žádné rigidní dramaturgické šablony (žádné 'Akt 1, Akt 2...'). Dva kolegové se baví naprosto přirozeně od jádra problému k technickému řešení a praktickým nuancím podle toho, co si dané téma samo žádá. Cílem je předat to podstatné, ne splnit formální strukturu.
2. DVĚ ROLE V DIALOGU:
   - "Petr" (Hlas: Fenrir) - Zkušený architekt, který věci reálně staví, opírá se o čísla, architekturu a technickou pravdu.
   - "Elena" (Hlas: Aoede) - Zvídavá kolegyně a praktička, která jde k věci, testuje limity, ptá se na rizika, náklady a klientskou realitu.
3. HLOUBKA & KONKRÉTNOST: Jděte přímo do hloubky. Konkrétní nástroje, parametry, JSON schémata, chybové kódy, vyjednávání smluv, tokenová ekonomika. Žádná povrchní vata.
4. KONTINUITA BEZ OPAKOVÁNÍ: Zákaz znovu od nuly vysvětlovat věci z předchozích lekcí nebo opakovat minulé příklady. Navažte přímo a přirozeně.

VÝSTUPNÍ JSON FORMÁT:
{{
  "module_index": {module_index},
  "title": "{module_title}",
  "estimated_duration_minutes": {duration_minutes},
  "summary_for_next_lessons": "Stručné shrnutí 2-3 klíčových témat a konkrétních příkladů, které zde zazněly, aby je další lekce neopakovala.",
  "turns": [
    {{
      "speaker": "Petr",
      "voice": "Fenrir",
      "text": "..."
    }},
    {{
      "speaker": "Elena",
      "voice": "Aoede",
      "text": "..."
    }}
  ]
}}
"""

def synthesize_turn_speech(text: str, voice_name: str, api_key: str, out_wav_path: str, retries: int = 3):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice_name
                    }
                }
            }
        }
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                raw_b64 = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
                pcm_bytes = base64.b64decode(raw_b64)
                
                with wave.open(out_wav_path, "wb") as wav_f:
                    wav_f.setnchannels(1)
                    wav_f.setsampwidth(2)
                    wav_f.setframerate(24000)
                    wav_f.writeframes(pcm_bytes)
                return True
        except Exception as e:
            time.sleep(2 ** attempt)
            if attempt == retries - 1:
                raise RuntimeError(f"Speech synthesis failed after {retries} attempts: {e}")

def assemble_audio_file(turns_wav_list: list, output_mp3_path: str, ffmpeg_path: str, pause_ms: int = 300):
    if not turns_wav_list:
        return
    with wave.open(turns_wav_list[0], 'rb') as first_w:
        params = first_w.getparams()
        framerate = first_w.getframerate()
        sampwidth = first_w.getsampwidth()
        nchannels = first_w.getnchannels()
    
    silence_bytes = b'\x00' * int(framerate * sampwidth * nchannels * (pause_ms / 1000.0))
    temp_merged_wav = output_mp3_path + ".temp.wav"

    with wave.open(temp_merged_wav, 'wb') as out_w:
        out_w.setparams(params)
        for idx, wav_file in enumerate(turns_wav_list):
            with wave.open(wav_file, 'rb') as in_w:
                data = in_w.readframes(in_w.getnframes())
                out_w.writeframes(data)
            if idx < len(turns_wav_list) - 1:
                out_w.writeframes(silence_bytes)
                
    cmd = [
        ffmpeg_path, "-y",
        "-i", temp_merged_wav,
        "-b:a", "192k",
        output_mp3_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_merged_wav):
        os.remove(temp_merged_wav)

def parse_module_selection(selection_str: str, total_modules: int) -> list:
    """Parses '1', '1,2', '1-3' into a list of 1-based module indices."""
    if not selection_str:
        return list(range(1, total_modules + 1))
    indices = set()
    parts = selection_str.split(",")
    for p in parts:
        p = p.strip()
        if "-" in p:
            start, end = p.split("-", 1)
            indices.update(range(int(start), int(end) + 1))
        elif p.isdigit():
            indices.add(int(p))
    return sorted([i for i in indices if 1 <= i <= total_modules])

def main():
    parser = argparse.ArgumentParser(description="Learning System Agent V3 - Batch Audio Studio (Humanized)")
    parser.add_argument("--course-dir", type=str, required=True, help="Directory containing the course (e.g. kurz-ai-agenti)")
    parser.add_argument("--duration", type=int, default=12, help="Target duration in minutes per lesson (default: 12)")
    parser.add_argument("--modules", type=str, default=None, help="Batch selection: single module (e.g. '1'), comma list ('1,2'), or milestone range ('1-3'). Default: all")
    parser.add_argument("--api-key", type=str, default=None, help="Google Gemini API Key")
    parser.add_argument("--skip-humanizer", action="store_true", help="Skip the Humanizer anti-slop pass")
    parser.add_argument("--dry-run-scripts", action="store_true", help="Only generate script JSONs without synthesizing audio")
    args = parser.parse_args()

    api_key = args.api_key or find_api_key()
    if not api_key:
        print("CHYBA: Nenašel jsem GEMINI_API_KEY. Nastav ho v prostředí nebo v .env souboru.")
        sys.exit(1)

    ffmpeg_path = find_ffmpeg()
    course_path = Path(args.course_dir)
    if not course_path.exists():
        print(f"CHYBA: Složka kurzu '{args.course_dir}' neexistuje.")
        sys.exit(1)

    curriculum_path = course_path / "kurikulum.txt"
    if not curriculum_path.exists():
        curriculum_path = course_path / "curriculum.txt"
    if not curriculum_path.exists():
        print(f"CHYBA: Nenalezen soubor kurikulum.txt v {course_path}")
        sys.exit(1)

    modules = []
    with open(curriculum_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                modules.append(line)

    if not modules:
        print("CHYBA: Kurikulum je prázdné.")
        sys.exit(1)

    selected_indices = parse_module_selection(args.modules, len(modules))

    # Read knowledge pack
    knowledge_pack_text = ""
    balicek_dir = course_path / "balicek"
    if balicek_dir.exists():
        for md_file in sorted(balicek_dir.glob("*.md")):
            try:
                with open(md_file, "r", encoding="utf-8") as mf:
                    knowledge_pack_text += f"\n\n--- {md_file.name} ---\n" + mf.read()
            except Exception:
                pass

    scripts_dir = course_path / "scripts"
    audio_dir = course_path / "audio"
    transcripts_dir = course_path / "transcripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    transcripts_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== LEARNING SYSTEM V3: BATCH AUDIO STUDIO ===")
    print(f"Kurz: {course_path.name}")
    print(f"Vybrané moduly (milník): {selected_indices} z celkových {len(modules)}")
    print(f"Délka lekce: ~{args.duration} minut")
    print(f"Struktura: Organický dialog bez rigidních šablon")
    print(f"Humanizer Pass: {'VYPNUT' if args.skip_humanizer else 'ZAPNUT (odstranění AI manýrů)'}")
    print(f"Audio Engine: Google Speech API (Petr: Fenrir, Elena: Aoede)")
    print(f"FFmpeg: {ffmpeg_path}")
    print("=" * 45)

    continuity_ledger = []

    # Pre-populate continuity from already finished earlier modules if any
    for prev_idx in range(1, len(modules) + 1):
        if prev_idx not in selected_indices and prev_idx < min(selected_indices):
            # Check if previous script exists to grab its summary
            matches = list(scripts_dir.glob(f"module_{prev_idx:02d}_*.json"))
            if matches:
                try:
                    with open(matches[0], "r", encoding="utf-8") as sf:
                        prev_data = json.load(sf)
                        s = prev_data.get("summary_for_next_lessons", "")
                        if s:
                            continuity_ledger.append(f"Modul {prev_idx}: {s}")
                except Exception:
                    pass

    for idx in selected_indices:
        mod_title = modules[idx - 1]
        safe_slug = "".join([c if c.isalnum() else "_" for c in mod_title])[:40].strip("_")
        script_file = scripts_dir / f"module_{idx:02d}_{safe_slug}.json"
        mp3_file = audio_dir / f"{idx:02d}_{safe_slug}.mp3"
        md_transcript_file = transcripts_dir / f"{idx:02d}_{safe_slug}.md"

        print(f"\n[Modul {idx}/{len(modules)}] {mod_title}")

        # Step 1: Generate or load script
        script_data = None
        if script_file.exists():
            print(f"  -> Skript již existuje v cache: {script_file.name}")
            try:
                with open(script_file, "r", encoding="utf-8") as sf:
                    script_data = json.load(sf)
            except Exception:
                pass

        if not script_data:
            print("  -> Generuji organický scénář zaměřený na předání podstaty...")
            prev_context = "\n".join(continuity_ledger)
            prompt = build_organic_script_prompt(
                module_title=mod_title,
                module_index=idx,
                total_modules=len(modules),
                previous_lessons_context=prev_context,
                knowledge_pack_content=knowledge_pack_text,
                duration_minutes=args.duration
            )
            script_data = call_gemini_json(prompt, api_key)

            # Step 1.5: Humanizer editing pass
            if not args.skip_humanizer and "turns" in script_data:
                print("  -> Humanizer pass: pročišťuji AI klišé, nucené trojice a chatbotové obraty...")
                script_data["turns"] = humanize_script_turns(script_data["turns"], api_key)

            with open(script_file, "w", encoding="utf-8") as sf:
                json.dump(script_data, sf, ensure_ascii=False, indent=2)
            print(f"  -> Scénář uložen ({len(script_data.get('turns', []))} replik)")

        summary = script_data.get("summary_for_next_lessons", "")
        if summary:
            continuity_ledger.append(f"Modul {idx} ({mod_title}): {summary}")

        # Markdown transcript
        with open(md_transcript_file, "w", encoding="utf-8") as mdf:
            mdf.write(f"# {idx:02d}. {mod_title}\n\n")
            mdf.write(f"*Délka: ~{args.duration} minut | Hlasy: Petr, Elena*\n\n---\n\n")
            for turn in script_data.get("turns", []):
                speaker = turn.get("speaker", "Host")
                text = turn.get("text", "")
                mdf.write(f"**{speaker}:** {text}\n\n")

        if args.dry_run_scripts:
            print("  -> Dry run: audio syntéza přeskočena.")
            continue

        # Step 2: Audio Synthesis
        if mp3_file.exists():
            print(f"  -> MP3 již existuje: {mp3_file.name}")
            continue

        print(f"  -> Syntetizuji přirozený hlas pro {len(script_data.get('turns', []))} replik...")
        turns = script_data.get("turns", [])
        turn_wavs = []
        temp_dir = audio_dir / f".tmp_{idx:02d}"
        temp_dir.mkdir(exist_ok=True)

        try:
            for t_idx, turn in enumerate(turns):
                voice = turn.get("voice", "Fenrir" if turn.get("speaker") == "Petr" else "Aoede")
                text = turn.get("text", "")
                turn_wav = temp_dir / f"turn_{t_idx:03d}.wav"
                
                print(f"     [{t_idx+1}/{len(turns)}] {turn.get('speaker')} ({voice})...", end="\r", flush=True)
                synthesize_turn_speech(text, voice, api_key, str(turn_wav))
                turn_wavs.append(str(turn_wav))

            print(f"\n  -> Sestavuji MP3 přes FFmpeg (192 kbps)...")
            assemble_audio_file(turn_wavs, str(mp3_file), ffmpeg_path, pause_ms=300)
            print(f"  -> HOTOVO: {mp3_file.name} ({os.path.getsize(mp3_file) // 1024} KB)")
        finally:
            for tw in turn_wavs:
                if os.path.exists(tw):
                    try:
                        os.remove(tw)
                    except Exception:
                        pass
            if temp_dir.exists():
                try:
                    os.rmdir(temp_dir)
                except Exception:
                    pass

    print("\n" + "=" * 45)
    print("DÁVKA VYBRANÝCH LEKCÍ DOKONČENA!")
    print(f"MP3 soubory: {audio_dir}")
    print(f"Transkripty: {transcripts_dir}")
    print("=" * 45)

if __name__ == "__main__":
    main()
