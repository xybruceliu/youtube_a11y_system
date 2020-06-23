import json, os, time, subprocess

def download_captions(video_id, path):

    out_path = path + video_id + ".vtt"
    url = "https://www.youtube.com/watch?v=" + video_id

    subprocess.call(['youtube-dl', "--no-playlist" , '--write-auto-sub', "--skip-download", '--sub-lang', 'en', 
                         '-o', out_path, url]) 

def str_to_s(ms):
    h,m,s = [float(l) for l in ms.split(":")]
    return s + float(m)*60.0 + float(h)*60.0*60.0


def process_captions(video_id, caption_path, words_path, tmp_base_path):
    if os.path.exists(caption_path) and not os.path.exists(words_path):
        print("Processing captions for: ", caption_path)
        all_words = []

        with open(caption_path) as f:
    
            lines = [l.replace("align:start position:0%", "").strip() for l in f.read().split("\n")]
            lines = [l for l in lines if "<c>" in l or "-->" in l]
            lines = [lines[i] for i in range(len(lines)-1) if "<c>" in lines[i] 
                     or ("-->" in lines[i] and "<c>" in lines[i+1])]
            lines = [l.replace("<c>", "").replace("</c>","") for l in lines]
            
            for i in range(0, len(lines)-1, 2):
                line_start, line_end = lines[i].split(" --> ")
                
                words = lines[i+1].split()
                current_start = line_start
                
                for j in range(len(words)):
                    # print(words[j].split("<"))
                    word = words[j].split("<")[0].strip() if "<" in words[j] else words[j]
                    end = words[j].split("<")[1].strip(">") if "<" in words[j] else line_end
                    
                    word_d = {
                        "word": word,
                        "alignedWord": word.lower(),
                        "start": str_to_s(current_start),
                        "end": str_to_s(end)
                    } 
                    
                    if str_to_s(end) - str_to_s(current_start) > 2.0:
                        #print(words[j], current_start, end, line_start, line_end)
                        word_d["end"] = str_to_s(current_start) + 2.0
                        
                    all_words.append(word_d)
                    current_start = end
        
        with open(words_path, "w") as fj:
            json.dump({"words": all_words}, fj)
            
        if not all_words:
            with open(caption_path) as f: 
                
                lines = [l.replace("align:start position:0%", "").strip() for l in f.read().split("\n") 
                         if l and "-->" not in l and "[" not in l][3:]
                txt = " ".join(lines)
                
                with open(tmp_base_path + video_id + ".txt", "w") as txtf:
                    txtf.write(txt)
                
                #print(txt)

def compute_non_dialog_percentage(video_id, video_dur, words_path, gaps_path):
    with open(words_path) as f: 
        words = json.load(f)["words"]

        if not words: 
            print(words_path)
            print("No words available")
            return 0
        
        else:
            twords = [{"end": 0}]  + words + [{"start": video_dur, "end": video_dur}]
            twords = [t for t in twords if not "case" in t.keys() or t["case"] != "not-found-in-audio"]

            gaps = []

            for i in range(1, len(twords)): 
                current_word = twords[i]
                prior_word = twords[i-1]
                
                gaps.append({"gap_start": current_word["start"],
                             "gap_end": prior_word["end"],
                             "gap_duration": current_word["start"] - prior_word["end"]})
                
            gaps = [g for g in gaps if g["gap_duration"] > 1.0]

            with open(gaps_path, "w") as f: 
                json.dump(gaps, f, indent=4)

            print("Total gap time: \t", round(sum([g["gap_duration"] for g in gaps]), 2))
            print("Video time: \t\t", round(twords[-1]["end"], 2))
            print("Percent gap time: \t",  round(sum([g["gap_duration"] for g in gaps]) * 100.0 / twords[-1]["end"],2))

            return sum([g["gap_duration"] for g in gaps]) / twords[-1]["end"]

