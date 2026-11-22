"""
Batch Audio Studio for Learning System Agent (V3)
Generates full 10-15 minute conversational audio podcasts in Czech using Google Gemini Speech API and FFmpeg.
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
    # Try system PATH
    try:
        res = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True, check=True)
        paths = res.stdout.strip().splitlines()
        if paths:
            return paths[0]
    except Exception:
        pass
    return "ffmpeg"

def find_api_key():
    # 1. Environment variable
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    
    # 2. Workspace .env search
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
                
                # Write standard 24kHz 16-bit mono WAV
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

def build_podcast_script_prompt(module_title: str, module_index: int, total_modules: int,
                                previous_lessons_context: str, knowledge_pack_content: str,
                                duration_minutes: int = 12) -> str:
    target_words = int(duration_minutes * 140)  # ~140 words per minute in spoken Czech
    min_turns = max(18, duration_minutes * 2)

    return f"""
Jsi špičkový audio scenárista a pedagogický architekt. Píšeš scénář pro {duration_minutes}-minutovou hloubkovou audio lekci (podcast) v češtině.

TÉMA TÉTO LEKCE (Modul {module_index}/{total_modules}):
"{module_title}"

ZNALOSTNÍ PODKLAD (Fakta, failure modes, architektura z balíčku):
{knowledge_pack_content[:15000]}

PŘEDCHOZÍ LEKCE A KONTINUITA (CO UŽ BYLO PROBRÁNO):
{previous_lessons_context if previous_lessons_context else "Toto je první úvodní lekce kurzu."}

STRIKTNÍ PRAVIDLA KONTINUITY A OBSAHU:
1. ŽÁDNÉ OPAKOVÁNÍ ZÁKLADŮ: Pokud předchozí lekce probírala určité příklady nebo pojmy, ZAKAZUJE SE je znovu od nuly vysvětlovat. Místo toho navaž přirozeným oslím můstkem ("Jak jsme minule vyřešili X, dnes...").
2. 4-AKTOVÁ STRUKTURA ({duration_minutes} minut = cca {target_words} slov, minimálně {min_turns} replik dialogu):
   - Akt 1: Realita & Pasti (proč naivní přístupy selhávají, reálné prověřené chyby z praxe).
   - Akt 2: Technický & architektonický rozbor (konkrétní mechanismy, schémata, co se přesně děje pod kapotou).
   - Akt 3: Ostrý sparring & námitky (druhý host napadá slabá místa: edge-casy, náklady, odmítnutí klientem, bezpečnost).
   - Akt 4: Exekuční akční krok (co má posluchač udělat zítra ráno krok za krokem).
3. FORMÁT MLUVY:
   - Dva moderátoři:
     * "Petr" (Hlas: Fenrir) - Zkušený architekt, drží odborný směr, data a architekturu.
     * "Elena" (Hlas: Aoede) - Bystrá praktička, zvídavá oponentka, klade námitky, žádá konkrétní čísla a příklady.
   - Přirozená mluvená spisovná čeština s přirozenou hovorovostí. Žádné knižní archaismy ("nebť", "pročež"), žádné AI fráze ("V dnešním dynamickém světě").
   - Každá replika musí mít reálný obsah, ne jen "Máš pravdu, Petře!".

VÝSTUPNÍ JSON FORMÁT:
Musíš vrátit POUZE validní JSON s touto strukturou:
{{
  "module_index": {module_index},
  "title": "{module_title}",
  "estimated_duration_minutes": {duration_minutes},
  "summary_for_next_lessons": "Stručné shrnutí 3-4 klíčových témat a příkladů, které v této lekci zazněly, aby je další lekce neopakovala.",
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

def assemble_audio_file(turns_wav_list: list, output_mp3_path: str, ffmpeg_path: str, pause_ms: int = 350):
    if not turns_wav_list:
        return
    
    # Read sample params from first file
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
                
    # Run ffmpeg to compress to 192kbps MP3
    cmd = [
        ffmpeg_path, "-y",
        "-i", temp_merged_wav,
        "-b:a", "192k",
        output_mp3_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(temp_merged_wav):
        os.remove(temp_merged_wav)

def main():
    parser = argparse.ArgumentParser(description="Learning System Agent V3 - Batch Audio Studio")
    parser.add_argument("--course-dir", type=str, required=True, help="Directory containing the course (e.g. kurz-ai-agenti)")
    parser.add_argument("--duration", type=int, default=12, help="Target duration in minutes per lesson (default: 12)")
    parser.add_argument("--api-key", type=str, default=None, help="Google Gemini API Key")
    parser.add_argument("--dry-run-scripts", action="store_true", help="Only generate script JSONs without synthesizing audio")
    parser.add_argument("--module", type=int, default=None, help="Generate only a single specific module index (1-based)")
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
        # Fallback to curriculum.txt
        curriculum_path = course_path / "curriculum.txt"
    if not curriculum_path.exists():
        print(f"CHYBA: Nenalezen soubor kurikulum.txt v {course_path}")
        sys.exit(1)

    # Read curriculum lines
    modules = []
    with open(curriculum_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                modules.append(line)

    if not modules:
        print("CHYBA: Kurikulum je prázdné.")
        sys.exit(1)

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

    # Setup output folders
    scripts_dir = course_path / "scripts"
    audio_dir = course_path / "audio"
    transcripts_dir = course_path / "transcripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    transcripts_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== LEARNING SYSTEM V3: BATCH AUDIO STUDIO ===")
    print(f"Kurz: {course_path.name}")
    print(f"Celkem modulů: {len(modules)}")
    print(f"Délka lekce: ~{args.duration} minut")
    print(f"Audio Engine: Google Gemini Speech API (Fenrir & Aoede)")
    print(f"FFmpeg: {ffmpeg_path}")
    print("=" * 45)

    continuity_ledger = []

    for idx, mod_title in enumerate(modules, start=1):
        if args.module is not None and idx != args.module:
            continue

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
            print("  -> Generuji 10-15 min detailní scénář s kontinuitou přes Gemini...")
            prev_context = "\n".join(continuity_ledger)
            prompt = build_podcast_script_prompt(
                module_title=mod_title,
                module_index=idx,
                total_modules=len(modules),
                previous_lessons_context=prev_context,
                knowledge_pack_content=knowledge_pack_text,
                duration_minutes=args.duration
            )
            script_data = call_gemini_json(prompt, api_key)
            with open(script_file, "w", encoding="utf-8") as sf:
                json.dump(script_data, sf, ensure_ascii=False, indent=2)
            print(f"  -> Scénář uložen ({len(script_data.get('turns', []))} replik)")

        # Record continuity summary
        summary = script_data.get("summary_for_next_lessons", "")
        if summary:
            continuity_ledger.append(f"Modul {idx} ({mod_title}): {summary}")

        # Save Markdown transcript
        with open(md_transcript_file, "w", encoding="utf-8") as mdf:
            mdf.write(f"# {idx:02d}. {mod_title}\n\n")
            mdf.write(f"*Cílová délka: {args.duration} minut | Hlasy: Petr (Fenrir), Elena (Aoede)*\n\n---\n\n")
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

        print(f"  -> Syntetizuji hlasy pro {len(script_data.get('turns', []))} replik...")
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

            print(f"\n  -> Sestavuji finální MP3 přes FFmpeg (192 kbps)...")
            assemble_audio_file(turn_wavs, str(mp3_file), ffmpeg_path, pause_ms=350)
            print(f"  -> HOTOVO: {mp3_file.name} ({os.path.getsize(mp3_file) // 1024} KB)")
        finally:
            # Clean up temp turn wavs
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
    print("VŠECHNY AUDIO LEKCE BYLY ÚSPĚŠNĚ VYGENEROVÁNY!")
    print(f"Výsledné MP3 soubory najdeš v: {audio_dir}")
    print(f"Textové transkripty najdeš v: {transcripts_dir}")
    print("=" * 45)

if __name__ == "__main__":
    main()
